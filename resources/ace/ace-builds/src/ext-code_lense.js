define("ace/ext/code_lense",["require","exports","module","ace/line_widgets","ace/lib/lang","ace/lib/dom","ace/editor","ace/config"], function(require, exports, module) {
"use strict";
var LineWidgets = require("../line_widgets").LineWidgets;
var lang = require("../lib/lang");
var dom = require("../lib/dom");

function clearLenseElements(renderer) {
    var textLayer = renderer.$textLayer;
    var lenseElements = textLayer.$lenses;
    if (lenseElements)
        lenseElements.forEach(function(el) {el.remove(); });
    textLayer.$lenses = null;
}

function renderWidgets(changes, renderer) {
    var changed = changes & renderer.CHANGE_LINES 
        || changes & renderer.CHANGE_FULL 
        || changes & renderer.CHANGE_SCROLL
        || changes & renderer.CHANGE_TEXT;
    if (!changed) 
        return;
    
    var session = renderer.session;
    var lineWidgets = renderer.session.lineWidgets;
    var textLayer = renderer.$textLayer;
    var lenseElements = textLayer.$lenses;
    if (!lineWidgets) {
        if (lenseElements)
            clearLenseElements(renderer);
        return;
    }

    var textCells = renderer.$textLayer.$lines.cells;
    var config = renderer.layerConfig;
    var padding = renderer.$padding;

    if (!lenseElements)
        lenseElements = textLayer.$lenses = [];


    var index = 0;
    for (var i = 0; i < textCells.length; i++) {
        var row = textCells[i].row;
        var widget = lineWidgets[row];
        var lenses = widget && widget.lenses;

        if (!lenses || !lenses.length) continue;

        var lenseContainer = lenseElements[index];
        if (!lenseContainer) {
            lenseContainer = lenseElements[index]
                = dom.buildDom(["div", {class: "ace_codeLense"}], renderer.container);
        }
        lenseContainer.style.height = config.lineHeight + "px";
        index++;

        for (var j = 0; j < lenses.length; j++) {
            var el = lenseContainer.childNodes[2 * j];
            if (!el) {
                if (j != 0) lenseContainer.appendChild(dom.createTextNode("\xa0|\xa0"));
                el = dom.buildDom(["a"], lenseContainer);
            }
            el.textContent = lenses[j].title;
            el.lenseCommand = lenses[j];
        }
        while (lenseContainer.childNodes.length > 2 * j - 1) 
            lenseContainer.lastChild.remove();

        var top = renderer.$cursorLayer.getPixelPosition({
            row: row,
            column: 0
        }, true).top - config.lineHeight * widget.rowsAbove - config.offset;
        lenseContainer.style.top = top + "px";
        
        var left = renderer.gutterWidth;
        var indent = session.getLine(row).search(/\S|$/);
        if (indent == -1)
            indent = 0;
        left += indent * config.characterWidth;
        left -= renderer.scrollLeft;
        lenseContainer.style.paddingLeft = padding + left + "px";
    }
    while (index < lenseElements.length)
        lenseElements.pop().remove();
}

function clearCodeLenseWidgets(session) {
    if (!session.lineWidgets) return;
    var widgetManager = session.widgetManager;
    session.lineWidgets.forEach(function(widget) {
        if (widget && widget.lenses)
            widgetManager.removeLineWidget(widget);
    });
}

exports.setLenses = function(session, lenses) {
    var firstRow = Number.MAX_VALUE;

    clearCodeLenseWidgets(session);
    lenses && lenses.forEach(function(lense) {
        var row = lense.start.row;
        var column = lense.start.column;
        var widget = session.lineWidgets && session.lineWidgets[row];
        if (!widget || !widget.lenses) {
            widget = session.widgetManager.$registerLineWidget({
                rowCount: 1,
                rowsAbove: 1,
                row: row,
                column: column,
                lenses: []
            });
        }
        widget.lenses.push(lense.command);
        if (row < firstRow)
            firstRow = row;
    });
    session._emit("changeFold", {data: {start: {row: firstRow}}});
    
    
};

function attachToEditor(editor) {
    var session = editor.session;
    if (!session.widgetManager) {
        session.widgetManager = new LineWidgets(session);
        session.widgetManager.attach(editor);
    }
    editor.renderer.on("afterRender", renderWidgets);
    editor.$codeLenseClickHandler = function(e) {
        var command = e.target.lenseCommand;
        if (command)
            editor.execCommand(command.id, command.arguments);
    };
    editor.container.addEventListener("click", editor.$codeLenseClickHandler);
    editor.$updateLenses = function() {
        var session = editor.session;
        if (!session) return;
        var codeLensProvider = session.codeLensProvider || session.$mode.codeLensProvider;
        var lenses = codeLensProvider && codeLensProvider.provideCodeLenses(session);
        
        var cursor = session.selection.cursor;
        var oldRow = session.documentToScreenRow(cursor);
        exports.setLenses(session, lenses);
        
        var lastDelta = session.$undoManager && session.$undoManager.$lastDelta;
        if (lastDelta && lastDelta.action == "remove" && lastDelta.lines.length > 1)
            return;
        var row = session.documentToScreenRow(cursor);
        var lineHeight = editor.renderer.layerConfig.lineHeight;
        var top = session.getScrollTop() + (row - oldRow) * lineHeight;
        session.setScrollTop(top);
    };
    var updateLenses = lang.delayedCall(editor.$updateLenses);
    editor.$updateLensesOnInput = function() {
        updateLenses.delay(250);
    };
    editor.on("input", editor.$updateLensesOnInput);
}

function detachFromEditor(editor) {
    editor.off("input", editor.$updateLensesOnInput);
    editor.renderer.off("afterRender", renderWidgets);
    if (editor.$codeLenseClickHandler)
        editor.container.removeEventListener("click", editor.$codeLenseClickHandler);
}

exports.setCodeLenseProvider = function(editor, codeLensProvider) {
    editor.setOption("enableCodeLense", true);
    editor.session.codeLensProvider = codeLensProvider;
    editor.$updateLensesOnInput();
};

exports.clear = function(session) {
    exports.setLenses(session, null);
};

var Editor = require("../editor").Editor;
require("../config").defineOptions(Editor.prototype, "editor", {
    enableCodeLense: {
        set: function(val) {
            if (val) {
                attachToEditor(this);
            } else {
                detachFromEditor(this);
            }
        }
    }
});

dom.importCssString("\
.ace_codeLense {\
    position: absolute;\
    color: #aaa;\
    font-size: 88%;\
    background: inherit;\
    width: 100%;\
    display: flex;\
    align-items: flex-end;\
    pointer-events: none;\
}\
.ace_codeLense > a {\
    cursor: pointer;\
    pointer-events: auto;\
}\
.ace_codeLense > a:hover {\
    color: #0000ff;\
    text-decoration: underline;\
}\
.ace_dark > .ace_codeLense > a:hover {\
    color: #4e94ce;\
}\
", "");

});                (function() {
                    window.require(["ace/ext/code_lense"], function(m) {
                        if (typeof module == "object" && typeof exports == "object" && module) {
                            module.exports = m;
                        }
                    });
                })();
            
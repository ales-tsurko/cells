define("ace/mode/matching_brace_outdent",["require","exports","module","ace/range"], function(require, exports, module) {
"use strict";

var Range = require("../range").Range;

var MatchingBraceOutdent = function() {};

(function() {

    this.checkOutdent = function(line, input) {
        if (! /^\s+$/.test(line))
            return false;

        return /^\s*\}/.test(input);
    };

    this.autoOutdent = function(doc, row) {
        var line = doc.getLine(row);
        var match = line.match(/^(\s*\})/);

        if (!match) return 0;

        var column = match[1].length;
        var openBracePos = doc.findMatchingBracket({row: row, column: column});

        if (!openBracePos || openBracePos.row == row) return 0;

        var indent = this.$getIndent(doc.getLine(openBracePos.row));
        doc.replace(new Range(row, 0, row, column-1), indent);
    };

    this.$getIndent = function(line) {
        return line.match(/^\s*/)[0];
    };

}).call(MatchingBraceOutdent.prototype);

exports.MatchingBraceOutdent = MatchingBraceOutdent;
});

define("ace/mode/supercollider_highlight_rules",["require","exports","module","ace/lib/oop","ace/mode/text_highlight_rules"], function(require, exports, module) {
"use strict";

  var oop = require("../lib/oop");
  var TextHighlightRules = require("./text_highlight_rules").TextHighlightRules;

  var SuperColliderHighlightRules = function() {

    this.$rules = {
      start: [{
        token: "keyword",
        regex: /\b(?:if|while|for|forBy|do|case|switch)\b/
      }, 
      {
        token: "keyword.var",
        regex: /\b(?:var|classvar)\b/
      }, 
      {
        token: "string.double",
        regex: /"/,
        push: [{
          token: "string.double",
          regex: /"/,
          next: "pop"
        }, {
          token: "constant.character.escape",
          regex: /\\./
        }, {
          defaultToken: "string.double"
        }]
      }, 
      {
        token: "string.symbol",
        regex: /'/,
        push: [{
          token: "string.symbol",
          regex: /'/,
          next: "pop"
        }, {
          token: "constant.character.escape",
          regex: /\\./
        }, {
          defaultToken: "string.symbol"
        }]
      }, 
      {
        token: "constant.character",
        regex: /\$./
      }, 
      {
        token: "entity.name.tag",
        regex: /[a-z][a-zA-Z0-9_]*\:/
      }, 
      {
        token: [
          "text",
          "entity.name.function",
          "text",
          "text",
          "text"
        ],
        regex: /^(\s*\+*\s*)([A-Z]{1}[a-zA-Z0-9_]*)(\s*\:{1}\s*)([A-Z]{1}[a-zA-Z0-9_]*)(\s*\{)/
      },
      {
        token: ["entity.name.function", "text"],
        regex: /^([A-Z_]{1}[a-zA-Z0-9_]*)([^a-zA-Z0-9_])/
      }, 
      {
        token: ["text", "variable.parameter"],
        regex: /({[\s]*)(\|)/,
        push: [{
          token: "variable.parameter",
          regex: /\|/,
          next: "pop"
        }, {
          defaultToken: "variable.parameter"
        }]
      }, 
      {
        token: ["text", "variable.parameter"],
        regex: /({[\s]*)(arg)/,
        push: [{
          token: "text",
          regex: /;/,
          next: "pop"
        }, {
          defaultToken: "variable.parameter"
        }]
      }, 
      {
        token: "keyword.operator",
        regex: /!|%|&|\*|\-|\+|==|=|!=|!=|<=|<!|>=|<|>|!|&&|\|\|/
      }, 
      {
        token: [
          "text",
          "entity.name.function",
          "text"
        ],
        regex: /([^a-zA-Z0-9\\])([A-Z_]{1}[a-zA-Z0-9_]*)([^a-zA-Z0-9_])/
      },
      {
        token: "constant.language",
        regex: /\b(?:inf|nil|true|false)\b/
      }, 
      {
        token: "string.symbol",
        regex: /\\[a-zA-Z0-9\_]+/
      }, 
      {
        token: [
          "text",
          "entity.name.function",
          "text"
        ],
        regex: /^(\s*)(\**[a-z]{1}[a-zA-Z0-9_]*)(\s*\{)/
      }, 
      {
        token: "variable.other",
        regex: /\~[a-zA-Z0-9_]+/
      }, 
      {
        token: "variable.language",
        regex: /\b(?:this|thisThread|thisMethod|thisFunction|thisProcess)\b/
      }, 
      {
        token: "comment.single",
        regex: /\/\/.*/
      }, 
      {
        token: "comment.multiline",
        regex: /\/\*/,
        push: [{
          token: "comment.multiline",
          regex: /\*\//,
          next: "pop"
        }, {
          defaultToken: "comment.multiline"
        }]
      }, 
      {
        token: "constant.numeric",
        regex: /\\b(0[xX][A-Fa-f0-9](?=(_?[A-Fa-f0-9]))\\2(?:)*|\\d(?=(_?\\d))\\3(?:)*(\\.(?!(?:[\\s]|[\\d]))(?=(_?\\d))\\5(?:)*)?([eE][-+]?\\d(?=(_?\\d))\\7(?:)*)?|0[bB][01]+)\\b/,
        comment: "Numbers"
      }
      ]
    };

    this.normalizeRules();
  };

  SuperColliderHighlightRules.metaData = {
    fileTypes: ["sc", "scd"],
    foldingStartMarker: "\\{|\\/\\*|\\(",
    foldingStopMarker: "\\}|\\*\\/|\\)",
    keyEquivalent: "^~S",
    name: "SuperCollider",
    scopeName: "source.supercollider"
  };


  oop.inherits(SuperColliderHighlightRules, TextHighlightRules);

  exports.SuperColliderHighlightRules = SuperColliderHighlightRules;
});

define("ace/mode/folding/cstyle",["require","exports","module","ace/lib/oop","ace/range","ace/mode/folding/fold_mode"], function(require, exports, module) {
"use strict";

var oop = require("../../lib/oop");
var Range = require("../../range").Range;
var BaseFoldMode = require("./fold_mode").FoldMode;

var FoldMode = exports.FoldMode = function(commentRegex) {
    if (commentRegex) {
        this.foldingStartMarker = new RegExp(
            this.foldingStartMarker.source.replace(/\|[^|]*?$/, "|" + commentRegex.start)
        );
        this.foldingStopMarker = new RegExp(
            this.foldingStopMarker.source.replace(/\|[^|]*?$/, "|" + commentRegex.end)
        );
    }
};
oop.inherits(FoldMode, BaseFoldMode);

(function() {
    
    this.foldingStartMarker = /(\{|\[)[^\}\]]*$|^\s*(\/\*)/;
    this.foldingStopMarker = /^[^\[\{]*(\}|\])|^[\s\*]*(\*\/)/;
    this.singleLineBlockCommentRe= /^\s*(\/\*).*\*\/\s*$/;
    this.tripleStarBlockCommentRe = /^\s*(\/\*\*\*).*\*\/\s*$/;
    this.startRegionRe = /^\s*(\/\*|\/\/)#?region\b/;
    this._getFoldWidgetBase = this.getFoldWidget;
    this.getFoldWidget = function(session, foldStyle, row) {
        var line = session.getLine(row);
    
        if (this.singleLineBlockCommentRe.test(line)) {
            if (!this.startRegionRe.test(line) && !this.tripleStarBlockCommentRe.test(line))
                return "";
        }
    
        var fw = this._getFoldWidgetBase(session, foldStyle, row);
    
        if (!fw && this.startRegionRe.test(line))
            return "start"; // lineCommentRegionStart
    
        return fw;
    };

    this.getFoldWidgetRange = function(session, foldStyle, row, forceMultiline) {
        var line = session.getLine(row);
        
        if (this.startRegionRe.test(line))
            return this.getCommentRegionBlock(session, line, row);
        
        var match = line.match(this.foldingStartMarker);
        if (match) {
            var i = match.index;

            if (match[1])
                return this.openingBracketBlock(session, match[1], row, i);
                
            var range = session.getCommentFoldRange(row, i + match[0].length, 1);
            
            if (range && !range.isMultiLine()) {
                if (forceMultiline) {
                    range = this.getSectionRange(session, row);
                } else if (foldStyle != "all")
                    range = null;
            }
            
            return range;
        }

        if (foldStyle === "markbegin")
            return;

        var match = line.match(this.foldingStopMarker);
        if (match) {
            var i = match.index + match[0].length;

            if (match[1])
                return this.closingBracketBlock(session, match[1], row, i);

            return session.getCommentFoldRange(row, i, -1);
        }
    };
    
    this.getSectionRange = function(session, row) {
        var line = session.getLine(row);
        var startIndent = line.search(/\S/);
        var startRow = row;
        var startColumn = line.length;
        row = row + 1;
        var endRow = row;
        var maxRow = session.getLength();
        while (++row < maxRow) {
            line = session.getLine(row);
            var indent = line.search(/\S/);
            if (indent === -1)
                continue;
            if  (startIndent > indent)
                break;
            var subRange = this.getFoldWidgetRange(session, "all", row);
            
            if (subRange) {
                if (subRange.start.row <= startRow) {
                    break;
                } else if (subRange.isMultiLine()) {
                    row = subRange.end.row;
                } else if (startIndent == indent) {
                    break;
                }
            }
            endRow = row;
        }
        
        return new Range(startRow, startColumn, endRow, session.getLine(endRow).length);
    };
    this.getCommentRegionBlock = function(session, line, row) {
        var startColumn = line.search(/\s*$/);
        var maxRow = session.getLength();
        var startRow = row;
        
        var re = /^\s*(?:\/\*|\/\/|--)#?(end)?region\b/;
        var depth = 1;
        while (++row < maxRow) {
            line = session.getLine(row);
            var m = re.exec(line);
            if (!m) continue;
            if (m[1]) depth--;
            else depth++;

            if (!depth) break;
        }

        var endRow = row;
        if (endRow > startRow) {
            return new Range(startRow, startColumn, endRow, line.length);
        }
    };

}).call(FoldMode.prototype);

});

define("ace/mode/supercollider",["require","exports","module","ace/lib/oop","ace/mode/text","ace/tokenizer","ace/mode/matching_brace_outdent","ace/mode/supercollider_highlight_rules","ace/mode/folding/cstyle","ace/mode/behaviour/cstyle"], function(require, exports, module) {
"use strict";

  var oop = require("../lib/oop");
  var TextMode = require("./text").Mode;
  var Tokenizer = require("../tokenizer").Tokenizer;
  var MatchingBraceOutdent = require("./matching_brace_outdent").MatchingBraceOutdent;
  var SuperColliderHighlightRules = require("./supercollider_highlight_rules").SuperColliderHighlightRules;
  var FoldMode = require("./folding/cstyle").FoldMode;
  var CstyleBehaviour = require("./behaviour/cstyle").CstyleBehaviour;

  var Mode = function() {
    this.HighlightRules = SuperColliderHighlightRules;
    this.$outdent = new MatchingBraceOutdent();
    this.$behaviour = new CstyleBehaviour({braces: true});
    this.foldingRules = new FoldMode();
  };
  oop.inherits(Mode, TextMode);

  (function() {
    this.lineCommentStart = "\/\/";
    this.blockComment = {start: "\/\*", end: "*\/"};

    this.getNextLineIndent = function(state, line, tab) {
      var indent = this.$getIndent(line);

      var tokenizedLine = this.getTokenizer().getLineTokens(line, state);
      var tokens = tokenizedLine.tokens;
      var endState = tokenizedLine.state;

      if (tokens.length && tokens[tokens.length-1].type == "comment") {
        return indent;
      }

      var match = line.match(/^.*(?:\bcase\b.*\:|[\{\(\[])\s*$/);
      if (match) {
        indent += tab;
      }

      return indent;
    };

    this.checkOutdent = function(state, line, input) {
      return this.$outdent.checkOutdent(line, input);
    };

    this.autoOutdent = function(state, doc, row) {
      this.$outdent.autoOutdent(doc, row);
    };

    this.$id = "ace/mode/supercollider";
  }).call(Mode.prototype);

  exports.Mode = Mode;
});

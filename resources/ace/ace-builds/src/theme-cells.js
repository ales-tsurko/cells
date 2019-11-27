define("ace/theme/cells",["require","exports","module","ace/lib/dom"], function(require, exports, module) {

exports.isDark = true;
exports.cssClass = "ace-cells";
exports.cssText = ".ace-cells .ace_gutter {\
background: #232126;\
color: rgb(144,140,147)\
}\
.ace-cells .ace_print-margin {\
width: 1px;\
background: #e8e8e8\
}\
.ace-cells {\
background-color: #232126;\
color: #FDF7FF\
}\
.ace-cells .ace_cursor {\
color: #FDF7FF\
}\
.ace-cells .ace_marker-layer .ace_selection {\
background: #392A46\
}\
.ace-cells.ace_multiselect .ace_selection.ace_start {\
box-shadow: 0 0 3px 0px #232126;\
border-radius: 2px\
}\
.ace-cells .ace_marker-layer .ace_step {\
background: rgb(198, 219, 174)\
}\
.ace-cells .ace_marker-layer .ace_bracket {\
margin: -1px 0 0 -1px;\
border: 1px solid #15111A\
}\
.ace-cells .ace_marker-layer .ace_active-line {\
background: #15111A\
}\
.ace-cells .ace_gutter-active-line {\
background-color: #15111A\
}\
.ace-cells .ace_marker-layer .ace_selected-word {\
border: 1px solid #392A46\
}\
.ace-cells .ace_fold {\
background-color: #48FCE3;\
border-color: #FDF7FF\
}\
.ace-cells .ace_keyword {\
color: #FF006A\
}\
.ace-cells .ace_constant.ace_language {\
color: #A560F3\
}\
.ace-cells .ace_constant.ace_numeric {\
color: #A560F3\
}\
.ace-cells .ace_constant.ace_character {\
color: #A560F3\
}\
.ace-cells .ace_constant.ace_other {\
color: #A560F3\
}\
.ace-cells .ace_support.ace_function {\
color: #0082FF\
}\
.ace-cells .ace_support.ace_constant {\
color: #0082FF\
}\
.ace-cells .ace_support.ace_class {\
font-style: italic;\
color: #0082FF\
}\
.ace-cells .ace_support.ace_type {\
font-style: italic;\
color: #0082FF\
}\
.ace-cells .ace_storage {\
color: #FF006A\
}\
.ace-cells .ace_storage.ace_type {\
font-style: italic;\
color: #0082FF\
}\
.ace-cells .ace_invalid {\
color: #FEF7FF;\
background-color: #D30099\
}\
.ace-cells .ace_invalid.ace_deprecated {\
color: #FEF7FF;\
background-color: #5B00C3\
}\
.ace-cells .ace_string {\
color: #FFBC41\
}\
.ace-cells .ace_comment {\
color: #646167\
}\
.ace-cells .ace_variable {\
color: #FDF7FF\
}\
.ace-cells .ace_variable.ace_parameter {\
font-style: italic;\
color: #FF7547\
}\
.ace-cells .ace_entity.ace_other.ace_attribute-name {\
color: #48FCE3\
}\
.ace-cells .ace_entity.ace_name.ace_function {\
color: #48FCE3\
}\
.ace-cells .ace_entity.ace_name.ace_tag {\
color: #FF006A\
}";

var dom = require("../lib/dom");
dom.importCssString(exports.cssText, exports.cssClass);
});                (function() {
                    window.require(["ace/theme/cells"], function(m) {
                        if (typeof module == "object" && typeof exports == "object" && module) {
                            module.exports = m;
                        }
                    });
                })();
            
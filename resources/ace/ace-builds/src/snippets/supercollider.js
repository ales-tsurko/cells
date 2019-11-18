define("ace/snippets/supercollider",["require","exports","module"], function(require, exports, module) {
  "use strict";

  exports.snippetText = "# do\n\
snippet do\n\
	do.({|${1}|\n\
		${2:// body}\n\
	});\n\
# Pbind\n\
snippet Pb\n\
	Pbind(\\instrument, \\\\${1:synth_name},\n\
		\\dur, ${2}\n\
	);\n\
# postln\n\
snippet po\n\
	(${1}).postln;\n\
# SynthDef\n\
snippet Sy\n\
	SynthDef(\"${1:name}\", {|${2:args}|\n\
		${3:// body}\n\
		Out.ar(${4:/*bus*/}, ${5:/* output */});\n\
	});\n\
# if\n\
snippet if\n\
	if {${1:true}} {\n\
		${2}\n\
	};\n\
# ife\n\
snippet ife\n\
	if {${1:true}} {\n\
		${2}\n\
	} {\n\
		${3:// else}\n\
	};\n\
# Routine\n\
snippet Rou\n\
	Routine({\n\
		${1:}\n\
	});\n\
# fork\n\
snippet fo\n\
	fork {\n\
		${1}\n\
	}\n\
";
  exports.scope = "supercollider";
});

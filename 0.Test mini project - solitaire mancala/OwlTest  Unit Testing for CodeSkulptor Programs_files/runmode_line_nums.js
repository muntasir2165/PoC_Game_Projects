CodeMirror.runMode = function(string, modespec, callback, options) {
	var mode = CodeMirror.getMode(CodeMirror.defaults, modespec);
	var lineNumber = 1; // Line number
	if (callback.nodeType == 1) {
		var tabSize = (options && options.tabSize)
				|| CodeMirror.defaults.tabSize;
		var node = callback, col = 0;
		node.innerHTML = "";
		callback = function(text, style) {

			if (text == "\n") {

				lineNumber++; //increment line number
				var lineNum = document.createTextNode(lineNumber+" "); // 

				node.appendChild(document.createElement("br"));

				node.appendChild(lineNum); // append
				col = 0;
				return;
			}
			var content = "";
			// replace tabs
			for ( var pos = 0;;) {
				var lineNum = document.createTextNode(lineNumber + " ")
				var idx = text.indexOf("\t", pos);
				if (idx == -1) {
					content += text.slice(pos);
					col += text.length - pos;

					break;
				} else {
					col += idx - pos;
					content += text.slice(pos, idx);
					var size = tabSize - col % tabSize;
					col += size;
					for ( var i = 0; i < size; ++i)
						content += " ";
					pos = idx + 1;

				}
			}

			if (style) {
				var sp = node.appendChild(document.createElement("span"));
				sp.className = "cm-" + style.replace(/ +/g, " cm-");
				sp.appendChild(document.createTextNode(content));
			} else {
				node.appendChild(document.createTextNode(content));
			}
		};
	}

	var lines = CodeMirror.splitLines(string), state = CodeMirror
			.startState(mode);
	for ( var i = 0, e = lines.length; i < e; ++i) {
		if (i)
			callback("\n");
		var stream = new CodeMirror.StringStream(lines[i]);
		while (!stream.eol()) {
			var style = mode.token(stream, state);
			callback(stream.current(), style, i, stream.start);
			stream.start = stream.pos;
		}
	}
	// add the first line
	var outputDiv = document.getElementById("tabs-code-text");
	var firstLine = document.createTextNode("1 ");
	outputDiv.insertBefore(firstLine, outputDiv.firstChild);
};
/**
 * Library for managing the results tabs for Owltest-based web pages (actually, the backend testing package)
 * Includes processing of the JSON-decoded results dictionary, called "msg_obj" below.
 * Format of msg_obj:
 * 
 *		msg_obj = {
 *			'score': score, 
 *			'max_score': max score,
 *			'student_filename': student filename,
 *			'student_code': student code body,
 *			'test_filename': test filename,    // only if verbosity=All
 *			'test_code': test code body, // only if verbosity=All
 *			'tabs': {       // may be absent if error_msg is present
 *				'tab_id': {
 *					'label': tab label,
 *					'msg_dicts': [{'pts':XX, 'msg':"..."]   // pts field may be missing if no points associated with message.
 *				}
 *			}
 *			'error_msg': error msg string    // not present for successful test run
 *		}
 *
 */
var OwlTest = OwlTest || {
	
	"TabManager" : (function($, window){
		
		/**
		 * Define implementation of TabManager, i.e. its constructor
		 * @param tabs_elt_id The id value of the overall tabs element
		 * @param student_URL The student_URL parameter given to the web page template.   Used to determine if the student code file is a CodeSkulptor or local file.
		 */ 
		var ManagerImpl = function(tabs_elt_id, student_URL){
			this.tabs_elt_id = "#"+tabs_elt_id;
			this.student_URL = student_URL;
			this.codeTabs = {};
			this.hideTabs();
		}
		
		/**
		 * The HTML, as a template, used to define a tab header
		 */
		var tabTemplate = "<li><a href='#{href}'>#{label}</a> </li>";
		
		/**
		 * Returns the jQuery element representing the tabs DOM element.
		 * This value cannot be saved as the DOM is changing as the tabs are 
		 * being built, so it must be recomputed at that the time that the
		 * that it is being used.   
		 */
		ManagerImpl.prototype.tabs_elt = function() {
			return $(this.tabs_elt_id);
		}
		
		
		/**
		 * Hides the tabs from view.
		 */
		ManagerImpl.prototype.hideTabs = function(){
			this.tabs_elt().hide(); 
		}
		
		/**
		 * Shows the tabs to the user.  
		 * @param active_idx The index of the tab to be activated.
		 */
		ManagerImpl.prototype.showTabs = function(active_idx){
			this.tabs_elt().tabs({active : active_idx});   // Set the active tab to the first one.
			this.tabs_elt().show(); // show the tabs now that there is content
		}
		
		
		/**
		 * Dynamically add a tab with the given id, label and content.
		 * Function is defined here so as to close over the tabs variable above.
		 * @param tab_id The id of the new tab
		 * @param label The label of the new tab
		 * @param tabContentHtml  The body of the new tab, as HTML. 
		 */
		ManagerImpl.prototype.addTab = function(tab_id, label, tabContentHtml) {
			var tabs = this.tabs_elt().tabs();
			var id = "tabs-" + tab_id;
			var li = $(tabTemplate.replace(/#\{href\}/g, "#" + id).replace(
					/#\{label\}/g, label));
	
			tabs.find(".ui-tabs-nav").append(li);
			//console.log("li = "+li)
			tabs.append('<div id="' + id + '"><div>' + tabContentHtml + '</div></div>');
	
			tabs.tabs("refresh");
	
	
			return id;
		}
		

		/**
		 * Sort the unsorted array by placing all string entities containing the given
		 * strings from a list of strings, sort_order, that determines what order the 
		 * unsorted strings are sorted. Any entities not that do not contain any 
		 * of the sort_order entries are simply tacked onto the result as is.
		 * @param unsorted_array The array to be sorted
		 * @param sort_order An array of string values that determine the sort order  
		 * @return The sorted array is returned.
		 */
		ManagerImpl.prototype.sortBy = function(unsorted_array, sort_order) {
			var unsorted = unsorted_array.slice();   // copy the original array into a destructable array.
			var sorted = []; // final order	
			for ( var so_idx in sort_order) { // loop over sort keywords
				for(var idx=unsorted.length-1; idx>=0; idx--){  // loop over remaining unsorted entities backwards to avoid deletion issues. 
					if (-1 != unsorted[idx].indexOf(sort_order[so_idx])) { // check if keyword is in unsorted
						sorted.push(unsorted[idx]); // append the entity onto the final list
						unsorted.splice(idx, 1); // remove the entity from the unsorted array
					}
	
				}
			}
			sorted = sorted.concat(unsorted); // copy the remainder of the unsorted entities
			return sorted;
		}
		
		var NO_BULLETS_MSGS = ["Comments", "Notes", "Feedback", "Submitted_File"];
		
		/**
		 * Add tabs from an dictionary of {tab_id:tab_msg_objs} where
		 * tab_id is the id for the new tab and 
		 * tab_msg_obj is {label: string, msgs:array_of_strings}
		 * where label is the label for the tab
		 * and msgs is the array of messages for that tab.
		 * @param msg_obj The message object containing the information to make the tabs  {"tabs":{tab_id:{label: "...", "msgs":[msg1, msg2,...]}}}
		 */
		ManagerImpl.prototype.addMsgTabs = function(msg_obj){
			
			var tab_info_dict = msg_obj.tabs;
			var tag_ids = Object.keys(tab_info_dict); // get the tag ids
			
			sorted_tag_ids = this.sortBy(tag_ids,  [ "Error", "Failure", "Warning" ]);// sort tab ids containing these words in the given order.
	
			for ( var idx in sorted_tag_ids) {
				tab_id = sorted_tag_ids[idx];
				msgs_str = "";
				if (0 <= NO_BULLETS_MSGS.indexOf(tab_id)) {
					
					for (i = 0; i < tab_info_dict[tab_id].msg_dicts.length; i++) {
						msg_dict = tab_info_dict[tab_id].msg_dicts[i];
						console.log("tab_id = "+tab_id+", label = "+tab_info_dict[tab_id].label);
						
						msgs_str += "<p style=\"white-space:pre-wrap\">";
						msgs_str +=	msg_dict["msg"]+"</p>";
					
					}
					
					tabContentHtml = msgs_str;
					
				}
				else {
					for (i = 0; i < tab_info_dict[tab_id].msg_dicts.length; i++) {
						msg_dict = tab_info_dict[tab_id].msg_dicts[i];
						msgs_str += "<li style=\"white-space:pre-wrap\">";
						if ("pts" in msg_dict) {
							msgs_str += "["+msg_dict["pts"].toFixed(1)+" pts] ";
						}
						msgs_str +=	msg_dict["msg"]+"</li>";
					}
					tabContentHtml = "<ol>" + msgs_str + "</ol>";
				}
				this.addTab(tab_id, tab_info_dict[tab_id].label, tabContentHtml);	
			}
		}
	
		/**
		 * Install read-only CodeMirror objects to handle the text of 
		 * all elements of the class "code" who are a children 
		 * of the element whose "id" is the given id.
		 * Returns a function of no parameters that refreshes all
		 * the CodeMirror objects associated with id.
		 * @param id The id of the tab containing the code in one of more sub-elements with class='code'. 
		 * @return A function of no parameters that will refresh all the code class sub-elements.
		 */
		ManagerImpl.prototype.installCodeMirror = function(id) {
			var cm_objs = [] // There might be more than one code class sub-element.
			$("#" + id + " .code").each(function() {
				var $this = $(this);
				var $code = $this.text();
				$this.empty();
				var codeMirrorObj = CodeMirror(this, {
					value : $code,
					mode : {
						name : "python",
						version : 2,
						singleLineStringErrors : false
					},
					lineNumbers : true,
					readOnly : true
				});
				cm_objs.push(codeMirrorObj);
			});
	
			// Need to return a function that refreshes all the associated CodeMirror objects.
			return function() {
				for (idx in cm_objs) {
					cm_objs[idx].refresh();
				}
			}
		}
		
		/**
		 * Add a tab containing the student code.   The this.student_URL field determines if the student code is a CodeSkulptor or local
		 * file.  If it is a CodeSkulptor file, the student filename will be hyperlinked to student_URL.
		 * The this.codeTabs dictionary field is set to map the new tab's id to the refresh function returned by installCodeMirror().
		 * @param msg_obj The message object holding the required data  {"student_filename": "...", "student_code": "..."}
		 */
		ManagerImpl.prototype.addStudentCodeTab = function(msg_obj){
			if ("student_filename" in msg_obj) {
				var tab_id = "student-code";
				var student_link = "";
				//console.log("student_URL = "+this.student_URL)
				if (this.student_URL) {
					//student_link = "<a target='_blank' href = 'http://www.codeskulptor.org/#"+ msg_obj.student_filename + "'>"
					student_link = "<a target='_blank' href = '"+this.student_URL + "'>"
								+ msg_obj.student_filename
								+ "</a>";
				}
				else {
					student_link = msg_obj.student_filename; 
				}
				var id = this.addTab(
						tab_id,
						"Your code",
						"<p>Filename: "+student_link+"</p><code><pre class = 'code' id = 'tabs-"+tab_id+"-text'>"
								+ msg_obj.student_code + "</pre></code>");
				this.codeTabs[id] = this.installCodeMirror(id); // install CodeMirror for the text and save the returned refresh function.
			}
		}
	
		/**
		 * Add a tab containing the test code
		 * The this.codeTabs dictionary field is set to map the new tab's id to the refresh function returned by installCodeMirror().
		 * @param msg_obj The message object holding the required data.
		 */
		ManagerImpl.prototype.addTestCodeTab = function(msg_obj){
			if ("test_filename" in msg_obj) {
				var tab_id = "test-code";
				var id = this.addTab(
						tab_id,
						"Test code",
						"<p>Filename: "
								+ msg_obj.test_filename
								+ "</p><code><pre class = 'code' id = 'tabs-"+tab_id+"-text'>"
								+ msg_obj.test_code + "</pre></code>");
				this.codeTabs[id] = this.installCodeMirror(id); // install CodeMirror for the text and save the returned refresh function.
			}
		}
		
		/**
		 * Install the event handler to refresh the CodeMirror objects on a tabs that contain them.
		 * Uses the this.codeTabs field to determine if a tab is contains CodeMirror instance(s) and the 
		 * related refresh function to refresh the code display. 
		 */
		ManagerImpl.prototype.setCodeTabEventHandler = function() {
			var self =this;   // Hack around "this" reference inside function below.
			// Attach an event handler to the tabs that will detect if a code tab is activated and tell CodeMirror to
			// refresh the associated code display.
			this.tabs_elt().on("tabsactivate", function(event, ui) {
				id = ui.newPanel.prop("id");
				if (id in self.codeTabs) {
					self.codeTabs[id](); // refresh the CodeMirror objects associated with id
				}
			});
		}
		
		
		/**
		 * Sets the score value on the page.
		 * @param element The page element that holds the score text.
		 * @param msg_obj The message object that holds the required data: {"score": value, "max_score": value}
		 */
		ManagerImpl.prototype.setScore = function(element, msg_obj){
			// compose the score string if it exists
			var score_str = "";
			if ("score" in msg_obj) {
				score_str = "<b>Score:</b>&nbsp;"
						+ msg_obj.score.toFixed(1)
						+ "/"
						+ msg_obj.max_score
						+ ((msg_obj.score < msg_obj.max_score) ? ""
								: "&nbsp;<b><em>Perfect score!</em> All tests pass. Great job!</b>");

				//element.html(score_str); // set the inner HTML text of the element with id="status"
			}
//			else {
//				element.html("");  // clear the element
//			}
			
			if ("score_comment" in msg_obj) {
				if (msg_obj.score_comment != null) {
					score_str += (score_str=="" ? "" : " ") +msg_obj.score_comment;
				}
			}
			element.html(score_str); // set the inner HTML text of the element with id="status"
		}
		
		/**
		 * Aggregate function that sets the score display, makes all the results messages tabs, the student code tab and if 
		 * present in msg_obj, the test code tab.    Installs the event handler to refresh the code tabs.
		 * @param msg_obj  The message object that holds all the required information.
		 */
		ManagerImpl.prototype.makeTabs = function(msg_obj){
		
			this.addMsgTabs(msg_obj); // add the result message tabs
			
			this.addStudentCodeTab(msg_obj);	
			
			if ("test_code" in msg_obj && "test_filename" in msg_obj){
				this.addTestCodeTab(msg_obj);
			}
		
			this.setScore($("#status"), msg_obj);
		
			this.setCodeTabEventHandler();
		}
			
		// Return Constructor object
		return ManagerImpl; 
	})(jQuery, window),
	
	"SubmitLock": (function($, window){
		/**
		 * Define convenience class to help prevent multiple submissions.  Only stops multiple submissions before 
		 * server responds with new page.  Resubmission lock-out releases after lock_time milliseconds if there is no 
		 * server response.  statusElt_id is the ID of an element with an innerText that 
		 */
		var SubmitLockImpl = function(statusElt_id, lock_time) {
			this._statusElt_id = statusElt_id; // Cannot get element yet because it may not be defined yet.
			this._wasSubmitted = false;
			this._submit_timeout = lock_time; //in milliseconds
		}
		
		/**
		 * Returns the current status of the submit lock.  True if the form was already submitted and false if not.
		 * The state of the lock will change to wasSubmitted()=true after wasSubmitted()=false for the length of the 
		 * lock_time given in the constructor.   A red warning message will be displayed if the submission was 
		 * already locked.
		 */
		SubmitLockImpl.prototype.wasSubmitted = function() {
			if(this._wasSubmitted) {
				getElt(this._statusElt_id).innerHTML += '  <span style="color:red">Already submitted, please wait...</span>';
				return true;
			}
			else {
				this._wasSubmitted = true;
				setTimeout(this._reset_wasSubmitted, this._submit_timeout);
				return false;
			}
		}
		
		/**
		 * Forcibly resets the submit lock to unsubmitted.   For internal use only.  Be careful about delayed execution of 
		 * this method by wasSubmitted().
		 */
		SubmitLockImpl.prototype._reset_wasSubmitted = function() {
			this._wasSubmitted = false;
		}
		
		// Return Constructor object
		return SubmitLockImpl;
	})(jQuery, window)
};


/**
 * Convenience wrapper for document.getElementById(id)
 */
function getElt(id) {
	return document.getElementById(id);
}

/**
 * Convenience function to help prevent multiple submissions.  Only stops multiple submissions before 
 * server responds with new page.  Resubmission lock-out releases after 10 seconds if there is no 
 * server response.
 * 
 * SHOULD THIS ALL BE ENCAPSULATED IN AN OBJECT?
 */
/*
var _submit_timeout = 10000; //in milliseconds
var _wasSubmitted = false;
function wasSubmitted(statusElt_id){
	if(_wasSubmitted) {
		getElt(statusElt_id).innerText += "  Already submitted, please wait...";
		return true;
	}
	else {
		_wasSubmitted = true;
		setTimeout(reset_wasSubmitted, _submit_timeout);
		return false;
	}
}

function reset_wasSubmitted() {
	_wasSubmitted = false;
}
*/

/**
 * Returns true if the given filename (no path) is a valid Python module name, i.e. conforms to the Python
 * spec for identifiers (https://docs.python.org/2/reference/lexical_analysis.html#identifiers). Returns false otherwise.  
 */
function checkPythonFilename(filename) {
	return (null != filename.match(/^[a-zA-Z_][a-zA-Z0-9_]*\.py$/));
}

/**
 * Validates the given form input (type="file") element, to make sure that the file is a valid Python file.
 * desc = a string description of the input element, to identify it.
 * Returns true if valid or if elt.value=="", false otherwise, including if more than one file is specified.
 * Does NOT check if the elt is required to have a value or not!
 * Pops up alert it invalid and returns focus to the element.
 * Clears the input element by rebuilding it because some browsers, i.e. IE, make the file input immutable as a security measure.
 * THE <INPUT TYPE="FILE"> ELEMENT *MUST* BE SURROUNDED BY <SPAN> TAG AND BE THE *ONLY* ELEMENT IN THE <SPAN> TAG!!
 */
function validatePythonFilename(elt, desc) {
	if(elt.value == "" || elt.files.length ==0) {
		return true;
	}
	else if(elt.files.length != 1) {
		alert("The "+desc+" input does not specify a single file.")
		return false;
	}
	else {
		result = checkPythonFilename(elt.files[0].name);
		if (!result) {
			var html = elt.parentNode.innerHTML // get the original HTML from the parent <span> tag.
	    	alert("The "+desc+" input has an invalid Python module name: \""+elt.files[0].name+"\" \nThe module's filename must start with a letter, contain only letters, numbers and/or underscores (\"_\") and end with \".py\".");
	    	elt.parentNode.innerHTML = html;  // reset the HTML, i.e. rebuild the element.
	    	elt.focus(); 
		}
		return result;
	}
}
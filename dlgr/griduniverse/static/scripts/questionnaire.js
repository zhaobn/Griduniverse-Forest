/*global Dallinger, submitAssignment */

import { DIFIInput } from 'identityfusion';


$(document).ready(function() {

  // Initialize DIFI widget
  var $DIFI = $('input.DIFI-input'),
      spinner = Dallinger.BusyForm();

  if ($DIFI.length) {
    var input = new DIFIInput(
      $DIFI.get(0),
      {
        groupLabel: $DIFI.attr('data-group-label'),
        groupImage: "static/images/colors/" + store.get("color") + ".png",
      }
    );
  }

  // Submit the questionnaire.
  $("#submit-questionnaire").click(function() {
    console.log("Submitting questionnaire.");
    var $elements = [$("form :input"), $(this)],
        questionSubmission = Dallinger.submitQuestionnaire("questionnaire");

    spinner.freeze($elements);
    questionSubmission.done(submitAssignment);
    questionSubmission.always(function () {
      spinner.unfreeze();
    });

  });

});

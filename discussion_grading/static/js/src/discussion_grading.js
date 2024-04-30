/* Javascript for XBlockDiscussionGrading. */
function XBlockDiscussionGrading(runtime, element) {
  const calculateGrade = runtime.handlerUrl(element, "calculate_grade");

  let gettext;
  if ("DiscussionGradingI18n" in window || "gettext" in window) {
    gettext = window.DiscussionGradingI18n?.gettext || window.gettext;
  }

  if (typeof gettext == "undefined") {
    // No translations -- used by test environment
    gettext = (string) => string;
  }

  $(element)
    .find("#calculate-grade")
    .click(function () {
      const data = {};
      $.post(calculateGrade, JSON.stringify(data))
        .done(function (response) {
          if (response.success) {
            window.location.reload();
          } else {
            $(element).find("#error-message").text(response.message);
          }
        })
        .fail(function () {
          console.log("Error calculating grade");
        });
    });
}

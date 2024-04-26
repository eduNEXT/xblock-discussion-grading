/* Javascript for XBlockDiscussionGrading. */
function XBlockDiscussionGrading(runtime, element) {
  const calculateGrade = runtime.handlerUrl(element, "calculate_grade");

  $(element)
    .find("#calculate-grade")
    .click(function () {
      const data = {};
      $.post(calculateGrade, JSON.stringify(data))
        .done(function (response) {
          $(element).find("#grade").text(`Your grade is ${response.weighted_score}`);
          console.log("User Stats", response.user_stats);
          console.log("Score", response.score);
          console.log("Weighted score", response.weighted_score);
        })
        .fail(function () {
          console.log("Error calculating grade");
        });
    });
}

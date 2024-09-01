$(document).ready(function () {
    $('#predictForm').on('submit', function (event) {
        event.preventDefault(); // Prevent default form submission
        var formateur = $('#formateur').val();
        var typef = $('#typef').val();
        var duration = $('#duration').val();
        var knowledge = $('#knowledge').val();
        var theme = $('#theme').val(); // Get theme value

        $.ajax({
            type: 'POST',
            url: '/',
            data: {
                formateur: formateur,
                typef: typef,
                duration: duration,
                knowledge: knowledge,
                theme: theme // Include theme in the data sent to Flask
            },
            success: function (data) {
                console.log("Response Data:", data); // Log response data
                let score = (data.overall_score + data.stars_rating) / 2;
                let perc = Math.round((score * 100) / 5);
                if (score < 0.8) {
                    $('#cmnt').html(`
                        <p class="cmnt vertical_line">The odds of success for this course with Mr./Ms.
                        ${formateur} are ${perc}%, indicating a very low likelihood of success.</p>
                    `);
                } else if (score < 2.5) {
                    $('#cmnt').html(`
                        <p class="cmnt vertical_line">The odds of success for this course with Mr./Ms.
                        ${formateur} are ${perc}%, indicating a moderate likelihood of success.</p>
                    `);
                } else if (score < 5) {
                    $('#cmnt').html(`
                        <p class="cmnt vertical_line">The odds of success for this course with Mr./Ms.
                        ${formateur} are ${perc}%, indicating a high likelihood of success.</p>
                    `);
                }
                $('#stars_rating').html(`
                    <p class="predicted_labels_headers">Stars Rating: <small> On scale of 5 </small></p>
                    <p class="predicted_values">${data.stars_rating}</p>
                `);

                $('#overall_score').html(`
                    <p class="predicted_labels_headers">Instructor matching: <small> On scale of 5 </small></p>
                    <p class="predicted_values">${data.overall_score}</p>
                `);
                $('#result').show(); // Show result div
            },
            error: function (xhr, status, error) {
                console.error("AJAX Error:", status, error); // Log AJAX error
            }
        });
    });
});

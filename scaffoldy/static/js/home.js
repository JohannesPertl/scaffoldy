$(document).ready(function () {
    const mainForm = $("#main-form");
    const downloadButton = $("#download-btn");
    const downloadSuccessSection = $("#download-success");
    const feedbackButtons = $('.create-feedback');
    const popovers = $('[data-toggle="popover"]');
    const url = window.location.href
    let contactHint = true;
    toggleCollapseForms();

    // Initialize all popovers
    popovers.popover({
        container: 'body',
    })

    // Disable contact hint if any feedback button has been clicked
    feedbackButtons.click(function () {
        contactHint = false;
    });

    if (url.includes('feedback')) {
        setTimeout(function () {
            $('#download-feedback-btn').click()
        }, 500);
    }

    // Gets triggered when element is in viewport
    $(window).scroll(function () {
        feedbackButtons.each(function () {
            if (contactHint) {
                if (isElementInViewport($(this))) {
                    let shown = $(this).hasClass("inViewport");
                    if (!shown) {
                        $(this).removeClass('enableHiding');
                        let timeout = 20000;

                        // Show feedback popover
                        setTimeout(() => {
                            if (!$(this).hasClass('disable-pop')) {
                                $(this).addClass('pop-trigger');
                            }
                            $(this).popover('show');
                            setTimeout(() => {
                                $(this).addClass('enableHiding');
                            }, 2000)
                        }, timeout);

                    }
                    $(this).addClass("inViewport");
                } else {
                    $(this).popover('hide');
                    $(this).removeClass("inViewport");
                    $(this).removeClass('pop-trigger');
                }
            }
        });
    });

    // Hide popovers on click, if they have been shown a time before
    $('body').on('click', function (e) {
        //buttons and icons within buttons
        if ($(e.target).data('toggle') !== 'popover'
            && $(e.target).parents('[data-toggle="popover"]').length === 0
            && $(e.target).parents('.popover.in').length === 0) {
            popovers.each(function () {
                if ($(this).hasClass('enableHiding')) {
                    console.log($(this));
                    $(this).popover('hide');
                }
            });
        }
    });

    feedbackButtons.click(function () {
        $(this).popover('hide');
        $(this).popover('disable');
        $(this).addClass('disable-pop');
    });

    downloadButton.click(function () {
        $(this).prop("disabled", true);
        // add spinner to button
        $(this).html(
            `<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Loading...`
        );

        $.ajax({
            data: mainForm.serialize(),
            type: mainForm.attr('method'),
            url: mainForm.attr('action'),
            success: function (response, status, jqXHR) {
                let contentType = jqXHR.getResponseHeader("content-type");
                if (jqXHR.status === 204 || contentType === "application/zip") {
                    // Valid form, go to download success section
                    downloadSuccessSection.removeClass("d-none");
                    $('#download-success-link').trigger("click");

                    // Reset download button to not loading
                    downloadButton.prop("disabled", false);
                    downloadButton.html(
                        `<i class="fa fa-download"></i> Download`
                    );
                }
                mainForm.submit()
            }
        });
    });


    // Don't show Generate Code Examples for specific programming language choices
    $('#id_programming_language').on('change', function () {
        const value = $('#id_programming_language').val();
        if (value === 'other') {
            $('#div_id_generate_code_examples').addClass('d-none');
            // $('#id_generate_code_examples').prop('checked', false);
        } else {
            $('#div_id_generate_code_examples').removeClass('d-none');
        }
    });


    $('#start-again-btn').click(function () {
        downloadSuccessSection.addClass("d-none");
        // clearForms();
        toggleCollapseForms();
    });


    $('.collapseFormButton').find("input").change(function () {
        toggleCollapseForms();
    });


    // Replace Skip button with Next button, if any checkbox of section is checked
    $("input[type='checkbox']").change(function () {
        let section = $(this).closest('section');
        let checkboxes = section.find('input[type=checkbox]:checked');
        let nextBtn = section.find('.next-btn');
        if (checkboxes.length > 0) {
            nextBtn.html('Next <i class="fa fa-arrow-down hvr-icon"></i>')
        } else {
            nextBtn.html('Skip <i class="fa fa-arrow-down hvr-icon"></i>')
        }
    });

});

function isElementInViewport(el) {

    // Special bonus for those using jQuery
    if (typeof jQuery === "function" && el instanceof jQuery) {
        el = el[0];
    }

    var rect = el.getBoundingClientRect();

    return (
        rect.top >= 0 &&
        rect.left >= 0 &&
        rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) && /* or $(window).height() */
        rect.right <= (window.innerWidth || document.documentElement.clientWidth) /* or $(window).width() */
    );
}

function clearForms() {
    $(':input').not(':button, :submit, :reset, :hidden, :checkbox, :radio').val('');
    $(':checkbox, :radio').prop('checked', false);
}


function toggleCollapseForms() {
    let collapseForms = $(".collapseForm");

    collapseForms.each(function () {
        let collapseCheckbox = $(this).find("input[id*='active']");
        let collapseTarget = $(this).find("div[id*='collapseTarget']");

        if (collapseCheckbox.is(':checked')) {
            collapseTarget.collapse('show');

            // Add required to FoldoutForm fields
            $('input', collapseTarget).each(function () {
                const requiredFields = ['database_name', 'username', 'password', 'port']
                const requiredID = $(this).attr('id')
                if (requiredFields.some(v => requiredID.includes(v))) {
                    $(this).prop('required', true);
                }
            })
        } else {
            collapseTarget.collapse('hide');

            // Remove required to FoldoutForm fields
            $('input', collapseTarget).each(function () {
                const requiredFields = ['database_name', 'username', 'password', 'port']
                const requiredID = $(this).attr('id')
                if (requiredFields.some(v => requiredID.includes(v))) {
                    $(this).prop('required', false);
                }
            })
        }
    });
}

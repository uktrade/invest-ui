dit.tagging.invest = new function() {

    this.init = function(page) {
        $(document).ready(function() {

            addTaggingForFeedbackLink();

            switch (page) {
                case 'InvestContactForm':
                    addTaggingForSubmitContactForm();
                    break;

                case 'InvestUkRegionPage':
                    addTaggingForAccordions();
                    break;

                case 'InvestIndustriesLandingPage':
                    addTaggingForIndustryCards();
                    break;

                case 'InvestIndustryPage':
                    addTaggingForAccordions();
                    addTaggingForRelatedIndustryCards();
                    break;

                case 'InvestLandingPage':
                    addTaggingForHeroCta();
                    addTaggingForEuExit();
                    addTaggingForFeaturedCards();
                    addTaggingForIndustryCards();
                    addTaggingForHPOs();
                    addTaggingForContactLink();
                    break;

                default: // do nothing
            }
        })
    };

    function addTaggingForFeedbackLink() {
        $("[data-ga-class='feedback-link']").on('click', function () {
            sendEvent(ctaEvent($(this).text(), 'Feedback'))
        });
    }

    function addTaggingForAccordions() {
        $("[data-ga-class='accordion']").on('click', function () {
            sendEvent(event('Toggle', 'Accordion', null, $(this).data('ga-value')))
        })
    }

    function addTaggingForSubmitContactForm() {
        $("[data-ga-class='contact-form']").on('submit', function () {
            sendEvent(event('Submit', 'Form', 'Contact', 'Submit'))
        })
    }

    function addTaggingForIndustryCards() {
        $("[data-ga-class='industry-link']").on('click', function () {
            sendEvent(ctaEvent($(this).data('ga-value'), 'Industries'))
        })
    }

    function addTaggingForRelatedIndustryCards() {
        $("[data-ga-class='card-link']").on('click', function () {
            sendEvent(ctaEvent($(this).data('ga-value'), 'RelatedIndustries'))
        })
    }

    function addTaggingForHeroCta() {
        $("[data-ga-class='hero-cta']").on('click', function () {
            sendEvent(ctaEvent($(this).text(), 'Hero'))
        })
    }

    function addTaggingForEuExit() {
        $("[data-ga-class='eu-exit-cta']").on('click', function () {
            sendEvent(ctaEvent($(this).text(), 'EuExit'))
        })
    }

    function addTaggingForFeaturedCards() {
        $("[data-ga-class='featured-cards']").on('click', function () {
            sendEvent(ctaEvent($(this).data('ga-value'), 'FeaturedCards'))
        })
    }

    function addTaggingForHPOs() {
        $("[data-ga-class='hpo-card']").on('click', function () {
            sendEvent(ctaEvent($(this).data('ga-value'), 'HPOs'))
        })
    }

    function addTaggingForContactLink() {
        $("[data-ga-class='contact-link']").on('click', function () {
            sendEvent(ctaEvent($(this).text(), 'Contact'))
        })
    }

    function ctaEvent(linkText, element) {
        return event("Link", "CTA", element, linkText)
    }

    function event(action, type, element, value) {
        var event = {
            'event': 'gaEvent',
            'action': action,
            'type': type,
            'value': value
        };

        if (element) {
            event.element = element;
        }

        return event;
    }

    function sendEvent(event) {
        window.dataLayer.push(event);
    }
};

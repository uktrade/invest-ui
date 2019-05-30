dit.tagging.invest = new function() {

    this.init = function(page) {
        $(document).ready(function() {
            switch (page) {
                case 'InvestContactForm':
                    addTaggingForFormSubmit();
                    break;

                case 'InvestHighPotentialOpportunityDetail':
                    addTaggingForContactCTA();
                    addTaggingForHPOVideo();
                    break;

                default: // do nothing
            }
        })
    };

    function addTaggingForFormSubmit() {
        $("[data-ga-class='contact-form']").on("submit", function() {
            window.dataLayer.push({
                'event': 'gaEvent',
                'action': 'Submit',
                'type': "Contact Form",
                'element': "Invest Contact Form",
                'value': $(this).text().trim()
            });
        })
    }

    function addTaggingForContactCTA() {
        $("[data-ga-class='contact-cta']").on("click", function() {
            window.dataLayer.push({
                'event': 'gaEvent',
                'action': 'Cta',
                'type': 'Contact',
                'element': 'Link',
                'value': $(this).text().trim()
            });
        })
    }

    function addTaggingForHPOVideo() {
        $("[data-ga-class='hpo-video']").on("play", function() {
            window.dataLayer.push({
                'event': 'gaEvent',
                'action': 'Play',
                'type': 'Video',
                'element': 'HPO Reasons To Invest',
            })
        });
    }
};

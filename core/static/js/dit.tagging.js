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
                'eventAction': 'Submit',
                'eventCategory': "Contact Form",
                'eventLabel': "Invest Contact Form",
                'eventValue': $(this).text().trim()
            });
        })
    }

    function addTaggingForContactCTA() {
        $("[data-ga-class='contact-cta']").on("click", function() {
            window.dataLayer.push({
                'eventAction': 'Cta',
                'eventCategory': 'Contact',
                'eventLabel': 'Link',
                'eventValue': $(this).text().trim()
            });
        })
    }

    function addTaggingForHPOVideo() {
        $("[data-ga-class='hpo-video']").on("play", function() {
            window.dataLayer.push({
                'eventAction': 'Play',
                'eventCategory': 'Video',
                'eventLabel': 'HPO Reasons To Invest',
            })
        });
    }
};

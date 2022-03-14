// toggle side catalog
$(".catalog-toggle").click((function (e) {
  e.preventDefault();
  $('.side-catalog').toggleClass("fold")
}));

// Navigation Scripts to Show Header on Scroll-Up
jQuery(document).ready(function ($) {
  var MQL = 1170;

  // primary navigation slide-in effect
  if ($(window).width() > MQL) {
      var bannerHeight = $("#catalog-hr").offset().top
      $(window).on('scroll', {
              previousTop: 0
          },
          function () {
              var currentTop = $(window).scrollTop(),
                  $catalog = $('.side-catalog');
              this.previousTop = currentTop;
              // adjust the appearance of side-catalog
              $catalog.show()
              if (currentTop > (bannerHeight - 10)) {
                  $catalog.addClass('fixed')
              } else {
                  $catalog.removeClass('fixed')
              }
          });
  }
});

$(document).ready(function () {
  tocbot.init({
      // Where to render the table of contents.
      tocSelector: '.catalog-body',
      // Where to grab the headings to build the table of contents.
      contentSelector: '.post-container',
      // Which headings to grab inside of the contentSelector element.
      headingSelector: 'h1, h2, h3, h4, h5',
      // For headings inside relative or absolute positioned containers within content.
      hasInnerContainers: true,
  });
});
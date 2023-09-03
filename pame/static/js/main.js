document.addEventListener('DOMContentLoaded', () => {
    const elementosCarousel = document.querySelectorAll('.carousel');
    M.Carousel.init(elementosCarousel, {
        duration: 120,
        dist: -80,
        shift: 5,
        padding: 5,
        numVisible: 5,
        indicators: false,
        noWrap: false,

    });
});
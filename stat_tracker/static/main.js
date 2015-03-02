(function($) {

    'use strict';
    // add your event handlers here

    var doMe = function () {
      console.log('doMe ran from within another closure');
    };

    // function doMe () {
    //   console.log('doMe ran');
    // }

    $(document).ready(function() {
        // add your event listeners here

        // this is broken, not sure why
        $(document).foundation();

        // if the other wasn't broken, this would 'bind' or 'live'
        // an event handler to the #someId DOM element
        $('#someId').on('click', doMe);


    });

}(jQuery));

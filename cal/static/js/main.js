/*
 * main.js
 * Copyright (C) 2016 rmad17 <souravbasu17@gmail.com>
 *
 * Distributed under terms of the MIT license.
 */
window.onload = function() {
    var updateBtn = document.getElementById("update-btn");
    var createBtn = document.getElementById("create-btn");

    updateBtn.addEventListener('click', function() {
        var inputs = [];
        $("div#events :input").each(function(){
            var input = $(this).val(); // This is the jquery object of the input, do what you will
            inputs.push(input);
        });
        console.log('i:', inputs);
        $.ajax({
            url: '',
                dataType: 'json',
                type: 'post',
                contentType: 'application/json',
                data: JSON.stringify({'data': inputs}),
                success: function( data, textStatus, jQxhr ){
                    console.log('data sent');
                    location.reload();
                },
                error: function( jqXhr, textStatus, errorThrown ){
                    console.log( errorThrown );
                }
            });
    }, false);

    createBtn.addEventListener('click', function() {
        var summary =  $('#create-input').val();
        $.ajax({
            url: 'create/',
                dataType: 'json',
                type: 'post',
                contentType: 'application/json',
                data: JSON.stringify({'data': summary}),
                success: function( data, textStatus, jQxhr ){
                    console.log('data sent');
                    location.reload();
                },
                error: function( jqXhr, textStatus, errorThrown ){
                    console.log( errorThrown );
                }
            });
    }, false);
};

(function($)
{
    $(document).ready(function()
    {
        var refreshId = setInterval(function()
        {
            $.post( "get_active_tasks/", "{}", function( data ) {
                  var items = [];

                  $.each( data["active_tasks"], function( key, val ) {
                    items.push( "<li>" + val.name+ "</li>" );
                  });

                  $("#active_tasks").html($( "<ul/>", {
                    "class": "task_list",
                    html: items.join( "" )
                  }));
                }, "json");
        }, 1000);
    });
})(jQuery);
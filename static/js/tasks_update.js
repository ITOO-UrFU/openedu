(function($)
{
    $(document).ready(function()
    {
        $.ajaxSetup(
        {
            type: "POST",
            cache: false,
            beforeSend: function() {

            },
            complete: function() {

            },
            success: function() {

            }
        });
        var $container = $("#active_tasks");
        $container.load("get_active_tasks/");
        var refreshId = setInterval(function()
        {
            $container.load("get_active_tasks/");
        }, 1000);
    });
})(jQuery);
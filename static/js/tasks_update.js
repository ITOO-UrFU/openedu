(function ($) {
    $(document).ready(function () {
        var refreshId = setInterval(function () {
            $.post("get_active_tasks/", "{}", function (data) {
                var items = [];
                if (data["active_tasks"].length != 0) {


                    $.each(data["active_tasks"], function (key, val) {
                        items.push("<li>" + val.name + "</li>");
                    });
                }
                else {
                    items.push("<p style='margin-left:1em'>Нет активных задач</p>")
                }

                $("#active_tasks").html($("<ul/>", {
                    "class": "task_list",
                    html: items.join("")
                }));
            }, "json");
        }, 3000);
    });
})(jQuery);
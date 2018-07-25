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
                    items.push("Нет активных задач")
                }

                $("#active_tasks").html($("<ul/>", {
                    "class": "task_list",
                    html: items.join("")
                }));
            }, "json");
        }, 1000);
    });
})(jQuery);
(function ($) {
    $(document).ready(function () {
        var refreshId = setInterval(function () {
            $.post("get_active_tasks/", "{}", function (data) {
                var items = [];
                if (data["active_tasks"].length != 0) {


                    $.each(data["active_tasks"], function (key, val) {
                        items.push("<tr><td>" + (parseInt(key)+1) + "</td>"+"<td>" + val.name + "</td>"+"<td>" + $.format.date(new Date(val.time_start*1000), 'dd/MM/yy HH:mm') + "</td></tr>");
                    });
                }
                else {
                    items.push("<p style='margin-left:2em'>Нет активных задач</p>")
                }

                $("#active_tasks_container tbody").html($("<tr/>", {
                    "class": "task_list",
                    html: items.join("")
                }));
            }, "json");
        }, 3000);
    });
})(jQuery);
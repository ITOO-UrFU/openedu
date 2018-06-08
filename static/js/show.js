var media_url = /uploads/
var url = "/openprofession/graphql?";
var fields_update_url = "/openprofession/update/";

var queries = {
    pdata_query: "{pdata(active:true){id,fio,birthDate,phone,email,quote,job,position,city,program{title, courseId},diplomaScan,claimScan,docForwarding,anotherDoc,programGrade,grades,createdAt,updatedAt,educationLevel,inQuote,paid,documentType,status,allDocs,allScans,allValid,docForwarding,possibleId}}",
    programs_query: "{programs{title,courseId,active,id,session}}",
    programs_unique_query: "{uniquePrograms}"
};



var app = new Vue({
    el: '#app',
     http: {
            emulateJSON: true,
            emulateHTTP: true
    },
    data: {
        pdata: [],
        programs: [],
        programs_for_show:[],
        pdata_for_show: [],
        error: null,
        only_active_programs: true,
        hiddenCols: [],
        sort_list: [],
        user_filters_options: ["by_program","by_docs", "quote", "inQuote", "paid", "allDocs", "allScans", "allValid"],
        user_filters: {
            by_program: {
                show_filter: false,
                all_programs: [],
                selected_values: []
            },
            by_docs: {
                show_filter: false,
                all_docs: ["claimScan", "diplomaScan", "docForwarding", "anotherDoc"],
                selected_values: []
            },
            quote: {
                show_filter: false,
                selected_values: [true, false]
            },
            inQuote: {
                show_filter: false,
                selected_values: [true, false]
            },
            paid: {
                show_filter: false,
                selected_values: [true, false]
            },
            allDocs: {
                show_filter: false,
                selected_values: [true, false]
            },
            allScans: {
                show_filter: false,
                selected_values: [true, false]
            },
            allValid: {
                show_filter: false,
                selected_values: [true, false]
            }
        }
    },
    created: function () {
        this.init();
    },

    filters: {
          moment: function (date) {
            return moment(date).format('DD.MM.YYYY, HH:mm');
          }
        },
        methods: {
        init: function () {
            this.hiddenCols = JSON.parse(localStorage.getItem('hiddenCols'));
            this.loadData();
            this.loadPrograms();
            this.loadUniqueProgramsNames();
        },
        loadData: function () {
            this.$http.get(url, {params:  {query: queries.pdata_query}} ).then((response) => {
                if(!!response.body)
            {
                this.pdata = JSON.parse(JSON.stringify(response.body.data.pdata));
                this.pdata_for_show = JSON.parse(JSON.stringify(this.pdata));
                console.log(this.pdata);
            }
        },
            (response) => {
                this.error = response;
            });
        },
        loadPrograms: function () {
        this.$http.get(url, {params:  {query: queries.programs_query}} ).then((response) => {
                if(!!response.body){
                    console.log("LOG: ", response.body.data.programs);
                    this.programs = response.body.data.programs;
                    this.programs_for_show = this.programs;
                    this.showActiveOnlyPrograms(this.only_active_programs);
            }
        },
            (response) => {
                this.error = response;
            });
        },
        loadUniqueProgramsNames: function () {
        this.$http.get(url, {params:  {query: queries.programs_unique_query}} ).then((response) => {
                if(!!response.body){
                    // console.log("LOG: ", );
                    this.user_filters.by_program.all_programs = JSON.parse(JSON.stringify(response.body.data.uniquePrograms));
                    this.user_filters.by_program.selected_values = JSON.parse(JSON.stringify(response.body.data.uniquePrograms));
                    // this.filterUsers();

                    // console.log(this.user_filters.by_program.all_programs);
                    // console.log(this.user_filters.by_program.checked_programs);
            }
        },
            (response) => {
                this.error = response;
            });
        },
        showActiveOnlyPrograms: function(item) {
            if (item) {
                this.programs_for_show = this.programs.filter(function (program) {
                    return program.active == true;
                });
            }
            else{
                this.programs_for_show = this.programs;
            }

        },
        changeField: function(event){
            var post_data = {
                "value": event.target.checked,
                "user_id": event.target.dataset.userId,
                "field_name": event.target.dataset.changeField,
                "local_field_name": event.target.dataset.localChangeField
            };
            var post_options = {
                headers: {
                    "X-CSRFToken": csrfToken
                }
            };
            this.$http.post(fields_update_url, post_data, post_options).then((response) => {
                this.showMessage(event.target, response.body);
                console.log(post_data);
                for (var i = 0; i < this.pdata.length; i++) {
                    if (this.pdata[i].id === post_data.user_id) {
                        console.log(this.pdata[i])
                        this.pdata[i][post_data.local_field_name] = post_data.value;
                    }
                }
            },
            (response) => {
                this.error = response;
                console.log(this.error);
            });
        },
        showMessage:function(target, response){
            var msg = document.createElement("div");

            if(response.result == "success") {
                msg.className = "alert alert-success";
                msg.innerHTML = "Сохранено";
            }
            else{
                msg.className = "alert alert-error";
                msg.innerHTML = "Ошибка";
            }
            target.closest('td').append(msg);
            setTimeout(function() {
                msg.remove();
            }, 1300);
        },
        sortByProperties:function(parametres){
            function dynamicSort(property) {
                var sortOrder = 1;
                if(property[0] === "-") {
                    sortOrder = -1;
                    property = property.substr(1);
                }
                return function (a,b) {
                    var result = (a[property] < b[property]) ? -1 : (a[property] > b[property]) ? 1 : 0;
                    return result * sortOrder;
                };
            }
            return this.pdata_for_show.sort(dynamicSort(parametres[0]));
        },

        sortByParam: function (param){
            console.log(this.sort_list)
            if(this.sort_list.includes(param)){
                var index = this.sort_list.indexOf(param);
                this.sort_list.splice(index, 1);
                this.sort_list.unshift("-"+param);
            }
            else if(this.sort_list.includes("-"+param)){
                var index = this.sort_list.indexOf("-"+param);
                this.sort_list.splice(index, 1);
            }
            else{
                this.sort_list.unshift(param);
            }
            if(this.sort_list.length > 0) {
                this.sortByProperties(this.sort_list);
            }
            else{
                console.log("KEK");
                this.pdata_for_show = JSON.parse(JSON.stringify(this.pdata));
                this.filterUsers();
            }
        },

        toggleFilterBLockVisible: function(filter_name){
            this.user_filters[filter_name].show_filter = !this.user_filters[filter_name].show_filter;
        },
        setProgramFilter: function (program_id) {
            var index = this.user_filters.by_program.selected_values.indexOf(program_id);
            console.log(index);
            if(index != -1){
                this.user_filters.by_program.selected_values.splice(index, 1);
            }
            else{
                this.user_filters.by_program.selected_values.push(program_id);
            }
            this.filterUsers();
            },
            setProgramFilterAll: function () {
                this.user_filters.by_program.selected_values = JSON.parse(JSON.stringify(this.user_filters.by_program.all_programs));
                this.filterUsers();
            },

            setProgramFilterNull: function () {
                this.user_filters.by_program.selected_values = [];
                this.filterUsers();
            },

            setFilter: function (filter_name, value) {
                var index = this.user_filters[filter_name].selected_values.indexOf(value);
                if(index != -1){
                    this.user_filters[filter_name].selected_values.splice(index, 1);
                }
                else{
                    this.user_filters[filter_name].selected_values.push(value);
                }
                this.filterUsers();

                // console.log(filter_name, value, this.user_filters[filter_name]);
            },

        filterUsers: function () {
            var return_data = JSON.parse(JSON.stringify(this.pdata));

            for (var i=0; i < this.user_filters_options.length; i++){

                filter_name = this.user_filters_options[i];
                selected_values = this.user_filters[filter_name].selected_values;
                console.log("::::::return_data",return_data);
                console.log("::::::!!!!!!!!!!!",filter_name, selected_values);
                if (filter_name=='by_program'){
                    return_data = return_data.filter(function (pd) {
                        return selected_values.includes(pd.program.courseId);
                    });
                }
                else if(filter_name=='by_docs'){
                    if(selected_values.length > 0) {
                        temp_data = [];
                        for (var i = 0; i < return_data.length; i++) {
                            if (selected_values.includes("claimScan")) {
                                if (return_data[i].claimScan == "") {
                                    continue;
                                }
                            }
                            if (selected_values.includes("anotherDoc")) {
                                if (return_data[i].anotherDoc == "") {
                                    continue;
                                }
                            }
                            if (selected_values.includes("diplomaScan")) {
                                if (return_data[i].diplomaScan == "") {
                                    continue;
                                }
                            }
                            if (selected_values.includes("docForwarding")) {
                                if (return_data[i].docForwarding == "") {
                                    continue;
                                }
                            }
                            temp_data.push(return_data[i]);
                        }
                        return_data = JSON.parse(JSON.stringify(temp_data));
                    }
                    else{
                        continue;
                    }
                }
                else{
                    console.log("::::::");
                    return_data = return_data.filter(function (pd) {
                        return selected_values.includes(pd[filter_name]);
                    });
                }
            }

            this.pdata_for_show = JSON.parse(JSON.stringify(return_data));
            }
        }
    });

$('#not_exists_reports').click(function () {
    $('#not_exists_reports_list').toggle();
});

$('#show_column_filters').click(function () {
    $('#filter').toggle();
});


  $('#mainTable').scroll(function(ev) {
    var fixed_cols_count = 1;
    $('thead th').css('transform', 'translateY(' + this.scrollTop + 'px)');
    $('thead th').slice(0,fixed_cols_count).css('transform', 'translateY(' + this.scrollTop + 'px) translateX(' + this.scrollLeft + 'px)');
    $('thead th').slice(0,fixed_cols_count).css('z-index', '10000');

    $('tbody .fixed-cell').css('transform', 'translateX(' + this.scrollLeft + 'px)');
  });


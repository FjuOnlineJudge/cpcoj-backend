function status_filter(status){
    let code = [["", "", ""],["", "none", "none"],["none", "", "none"],["none", "none", ""]];

    if(element = document.getElementsByClassName("Scheduled")){
        for(let i = 0; i < element.length; i++){
            element[i].style.display = code[status][0];
        }
    }
    if(element = document.getElementsByClassName("Running")){
        for(let i = 0; i < element.length; i++){
            element[i].style.display = code[status][1];
        }
    }
    if(element = document.getElementsByClassName("Ended")){
        for(let i = 0; i < element.length; i++){
            element[i].style.display = code[status][2];
        }
    }
};

function problem_name_filter(){
    let input, filter, tr, td, txtValue;
    input = document.getElementById("problem_name_input");
    filter = input.value.toUpperCase();
    tr = $("table tbody tr");

    for(let i = 0; i < tr.length; i++){
        td = tr[i].getElementsByTagName("td")[1];
        console.log(tr[i].getElementsByTagName("td"));
        if(td){
            txtValue = td.textContent || td.innerText;
            if(txtValue.toUpperCase().indexOf(filter) > -1){
                tr[i].style.display = "";
            }
            else{
                tr[i].style.display = "none";
            }
        }
    }
};

function add_problem_row(){

    if(typeof add_problem_row.problem_num == 'undefined'){
        add_problem_row.problem_num = 1;
    }
    
    console.log(add_problem_row.problem_num);

    
    $("#create_problem").append('<div class="form-inline" id="problem_${ ++add_problem_row.problem_num }">\
            <input type="text" class="form-control mx-sm-3 mb-2" >\
            <div class="Create_Contest_Problem_Name mb-2"></div>\
        </div>');
}

function get_problem() {
    if(typeof this.flag == 'undefined'){
        this.flag = false;
    }

    if(this.flag == false){
        $.ajax({
            type: "GET",
            url: `/contest/getproblem`,
            dataType: "json"
        })
        .done(function (json) {
            if(json["result"] != "success") {
                console.error("Get problem failed: ", json["message"]);
            }
            else {
                problems = json["data"]["problem_info"];

                for(let i = 0; i < problems.length; i++){
                    $("#modal-Addproblem").append(`
                        <div class="form-check">
                            <input class="form-check-input checkbox-problem" type='checkbox' id='problem_${ problems[i].problem_id }' value="#${ problems[i].problem_id } - ${ problems[i].problemName }">
                            <label class="form-check-label" for="problem_${ problems[i].problem_id }">
                                #${ problems[i].problem_id } - ${ problems[i].problemName }
                            </label>\
                        </div>\
                    `);
                }
            }
        })
        .fail(function (xhr, status, err) {

        })

        flag = true;
    }
};

function checked_box(){
    let element, cnt = 1;

    document.getElementById('form-problem').innerHTML = '';

    element = document.getElementsByClassName('checkbox-problem');

    for(let i = 0; i < element.length; i++){
        if(element[i].checked){
            $("#form-problem").append(`
                <div class="form-group row">
                    <label class="col-sm-1 col-form-label"><b>${ cnt }</b></label>
                    <div class="col-sm-5">
                        <input type="text" class="form-control" value="${ element[i].value }"  name="problem_${ cnt++ }" readonly>
                    </div>
                </div>
            `)
        }
    }
    $("#form-problem").append(`
        <input type="hidden" value="${ cnt-1 }"  name="problem_num">
    `)
};

$(document).ready(function() {

    $("#problem_name_input").keyup(function() {
        problem_name_filter();
    });
});




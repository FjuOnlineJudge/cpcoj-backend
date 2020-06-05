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

$(document).ready(function() {

$("#problem_name_input").keyup(function() {
    problem_name_filter();
});

});

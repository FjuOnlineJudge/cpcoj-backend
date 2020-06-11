function ChangeTab(evt, TabName) {
    // Declare all variables
    var i, tabcontent, tablinks;
  
    // Get all elements with class="tabcontent" and hide them
    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
      tabcontent[i].style.display = "none";
    }
  
    // Get all elements with class="tablinks" and remove the class "active"
    tablinks = document.getElementsByClassName("tablinks");
    for (i = 0; i < tablinks.length; i++) {
      tablinks[i].className = tablinks[i].className.replace(" active", "");
    }
  
    // Show the current tab, and add an "active" class to the button that opened the tab
    document.getElementById(TabName).style.display = "block";
    evt.currentTarget.className += " active";
};

function ChangeTab_Problem(evt, TabName) {
    // Declare all variables
    var i, tabcontent, tablinks;
  
    // Get all elements with class="tabcontent" and hide them
    tabcontent = document.getElementsByClassName("tabcontent_problem");
    for (i = 0; i < tabcontent.length; i++) {
      tabcontent[i].style.display = "none";
    }
  
    // Get all elements with class="tablinks" and remove the class "active"
    tablinks = document.getElementsByClassName("tablinks_problem");
    for (i = 0; i < tablinks.length; i++) {
      tablinks[i].className = tablinks[i].className.replace(" active", "");
    }
  
    // Show the current tab, and add an "active" class to the button that opened the tab
    document.getElementById(TabName).style.display = "block";
    evt.currentTarget.className += " active";
};

function get_rank(cid){
  $.ajax({
    type: "GET",
    url: `/contest/getrank/${cid}`,
    dataType: "json"
  })
  .done(function (json) {
      if(json["result"] != "success") {
          console.error("Get Rank failed: ", json["message"]);
      }
      else {
        document.getElementById('table-rank').innerHTML = '';
        rank = json['data'];

        let cnt = 1

        for(let i = 0; i < rank.length; i++){
            console.log(rank[i].problems)
            str = `
            <tr>
                <td>${ cnt++ }</td>
                <td>${ rank[i].user_name }</td>
                <td>${ rank[i].AC_num }</td>
                <td>${ rank[i].penalty }</td>
            `;
            
            for(let problem in rank[i].problems){
                if(rank[i].problems[problem].AC_time == '-1'){
                    if(rank[i].problems[problem].Wrong_num != 0)
                        str += `<td width=5% style="background-color:#E87272"> ${ rank[i].problems[problem].Wrong_num } try</td>`
                    else{
                        `<td width=5%></td>`
                    }
                }
                else{
                    str += `<td width=5% style="background-color:#60E760"> ${ rank[i].problems[problem].AC_time }/${ rank[i].problems[problem].Wrong_num+1 }</td>`
                }
            }

            str += '</tr>';
            $("#table-rank").append(str);
        }
      }
  })
  .fail(function (xhr, status, err) {

  })
}

function setProblems(){

};

$(document).ready(function() {
    setProblems();
});

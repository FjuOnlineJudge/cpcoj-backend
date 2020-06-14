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
                <td style="text-align: center;">${ rank[i].AC_num }</td>
                <td style="text-align: right;">${ rank[i].penalty }</td>
            `;
            
            for(let problem in rank[i].problems){
                if(rank[i].problems[problem].AC_time == '-1'){
                    if(rank[i].problems[problem].Wrong_num != 0)
                        str += `<td style="text-align: center; padding: 0"> 
                                    <div style="background-color:#E87272; text-align: center; margin: 0 auto; width:65px; height:48px">
                                        ${ rank[i].problems[problem].Wrong_num } try
                                    </div>
                                </td>`
                    else{
                        `<td><div></div></td>`
                    }
                }
                else{
                    str += `<td style="text-align: center; padding: 0"> 
                                <div style="background-color:#60E760; text-align: center; margin: 0 auto; width:65px;  height:48px">
                                    ${ rank[i].problems[problem].AC_time }/${ rank[i].problems[problem].Wrong_num+1 }
                                </div>
                            </td>`
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

function setProblems(cid, csrf_token){
    $.ajax({
        type: "GET",
        url: `/contest/setproblem/${cid}`,
        dataType: "json"
      })
      .done(function (json) {
        if(json["result"] != "success") {
            console.error("Get Problem failed: ", json["message"]);
        }
        else {
            problem_list = json['data']

            for(let i = 0; i < problem_list.length; i++){
                console.log(problem_list[i])
                var re = new RegExp('\n', 'g');

                if(i == 0)
                    str = `<div id="Problem_${ i+1 }" class="tabcontent_problem" style="display: block">`;
                else
                    str = `<div id="Problem_${ i+1 }" class="tabcontent_problem" style="display: none">`

                str +=`
                    <div class="row">
                        <div class="col-md-1 col-sm-1 col-lg-1 col-xl-1 dis"></div>
                        <div class="col-md-6 col-sm-6 col-lg-6 col-xl-6 dis">
                            <h1>${ problem_list[i]['problem_name'] }</h1>
                        </div>
                        <div class="col-md-1 col-sm-1 col-lg-1 col-xl-1 dis"></div>
                        <div class="col-md-1 col-sm-1 col-lg-1 col-xl-1 dis">
                            <button type="button" class="btn btn-primary" data-toggle="modal" data-target="#problem_${problem_list[i]['pid']}">
                                Submit
                            </button>
                            <div class="modal fade" id="problem_${problem_list[i]['pid']}" tabindex="-1" role="dialog" aria-labelledby="problem_${problem_list[i]['pid']}" aria-hidden="true">
                                <div class="modal-dialog" role="document">
                                    <div class="modal-content">
                                    <div class="modal-header">
                                        <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                                        <span aria-hidden="true">&times;</span>
                                        </button>
                                    </div>
                                    <div class="modal-body">
                                        <div class="row">
                                            <div class="col-md-12">
                                                <form method="POST" >
                                                    <input type="hidden" name="csrf_token" value="${ csrf_token }"/>
                                                    <div class="form-group dis page-title">
                                                        <label for="probID">
                                                            Problem ID
                                                        </label>
                                                        <input type="text" name="probID" id="probID" value="${ problem_list[i]['pid'] }" class="col-md-2 form-control" >
                                                    </div>
                                                    <div class="form-group dis page-title">
                                                        <label>
                                                            Language
                                                        </label>
                                                        <div class="form-check option_text">
                                                            <input type="radio" name="lang" id="lang_cpp" value="cpp" class="form-check-input" required checked>
                                                            <label class="form-check-label" for="lang_cpp">C++</label>
                                                        </div>
                                                        <div class="form-check option_text">
                                                            <input type="radio" name="lang" id="lang_c" value="c" class="form-check-input" disabled>
                                                            <label class="form-check-label" for="lang_c">C</label>
                                                        </div>
                                                    </div>
                                                    <div class="form-group page-title">
                                                        <label for="codeArea">
                                                            Code:
                                                        </label>
                                                        <textarea class="form-control" name="code" id="codeArea" rows="10"></textarea>
                                                    </div>
                                                    <input type="submit" class="btn btn-primary code-form-margin-bottom" value="Submit">
                                                </form>
                                            </div>
                                        </div>
                                    </div>

                                    </div>
                                </div>
                            </div>
                        </div>
                        

                        <div class="col-md-1 col-sm-1 col-lg-1 col-xl-1 dis"></div>
                        <div class="col-md-1 col-sm-1 col-lg-1 col-xl-1 dis"></div>
                        <div class="col-md-1 col-sm-1 col-lg-1 col-xl-1 dis"></div>
                        
                        
                        <div class="col-md-1 col-sm-1 col-lg-1 col-xl-1 dis"></div>
                        <div class="col-md-10 col-sm-10 col-lg-10 col-xl-10 dis">
                            <div class="card">
                                <div class="card-header title" style="text-align: center;">
                                    <h3 class="no-margin">Description</h3>
                                </div>
                                <div class="card-body text">
                                    ${ problem_list[i]['info']['description'].replace(re, "<br />")}
                                </div>
                            </div>
                        </div>
                        <div class="col-md-1 col-sm-1 col-lg-1 col-xl-1 dis"></div>
            
                        <div class="col-md-1 col-sm-1 col-lg-1 col-xl-1 dis"></div>
                        <div class="col-md-5 col-sm-5 col-lg-5 col-xl-5 dis">
                            <div class="card">
                                <div class="card-header title" style="text-align: center;">
                                    <h3 class="no-margin">Input Format</h3>
                                </div>
                                <div class="card-body text">
                                    ${ problem_list[i]['info']['input_format'].replace(re, "<br />") }
                                </div>
                            </div>
                        </div>
                        <div class="col-md-5 col-sm-5 col-lg-5 col-xl-5 dis">
                            <div class="card">
                                <div class="card-header title" style="text-align: center;">
                                    <h3 class="no-margin">Output Format</h3>
                                </div>
                                <div class="card-body text">
                                    ${ problem_list[i]['info']['output_format'].replace(re, "<br />") }
                                </div>
                            </div>
                        </div>
                        <div class="col-md-1 col-sm-1 col-lg-1 col-xl-1 dis"></div>
            
                        <div class="col-md-1 col-sm-1 col-lg-1 col-xl-1 dis"></div>
                        <div class="col-md-5 col-sm-5 col-lg-5 col-xl-5 dis">
                            <div class="card">
                                <div class="card-header title" style="text-align: center;">
                                    <h3 class="no-margin">Sample Input</h3>
                                </div>
                                <div class="card-body text">
                                    ${ problem_list[i]['info']['sample_input'].replace(re, "<br />") }
                                </div>
                            </div>
                        </div>
                        <div class="col-md-5 col-sm-5 col-lg-5 col-xl-5 dis">
                            <div class="card">
                                <div class="card-header title" style="text-align: center;">
                                    <h3 class="no-margin">Sample Output</h3>
                                </div>
                                <div class="card-body text">
                                    ${ problem_list[i]['info']['sample_output'].replace(re, "<br />") }
                                </div>
                            </div>
                        </div>
                        <div class="col-md-1 col-sm-1 col-lg-1 col-xl-1 dis"></div>
                    </div>
                </div>
                `

                $('#contest_problem').append(str)
            }
            
        }
      })
      .fail(function (xhr, status, err) {
      });

    

    
};

$(document).ready(function() {
    
});

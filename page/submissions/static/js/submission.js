var timerDict = {};

function random_string() {
    return Math.random().toString(36).substring(2);
}

function setResult(id, // submission id
        result,        // AC, WA, CE
        resultMsg,     // Result message
        info)          // Info dict from submission api
{
    let result_html = "";
    if (result == "AC")
        result_html = `<td id="${id}-result" class="ac-style">AC</td>`;
    else if (result == "WA")
        result_html = `<td id="${id}-result" class="wa-style">WA</td>`;
    else if (result == "CE")
        result_html = `
        <td id="${id}-result" class="ce-style" data-toggle="modal" data-target="#CEModal-${id}">CE</td>
        <div class="modal fade" id="CEModal-${id}" tabindex="-1" role="dialog" aria-labelledby="CEModalLabel"
            aria-hidden="true">
            <div class="modal-dialog" role="document">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title" id="CEModalLabel">Submission #${id}</h5>
                        <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                            <span aria-hidden="true">&times;</span>
                        </button>
                    </div>
                    <div class="modal-body">
                        <pre>${resultMsg}</pre>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-primary" data-dismiss="modal">Close</button>
                    </div>
                </div>
            </div>
        </div>`;
    else
        result_html = `<td id="${id}-result">${result}</td>`
    // Replace result
    $(`#${id}-result`).replaceWith(result_html);
    $(`#${id}-memory`).text(info["memory"]);
    console.log(typeof info["runtime"]);
    $(`#${id}-runtime`).text(info["runtime"].toFixed(2));
}

function checkResult(id) {
    $.ajax({
        type: "GET",
        url: `/api/submission/${id}`,
        dataType: "json"
    })
    .done(function (json) {
        console.log(json);
        if(json["result"] != "success")
        {
            console.error("Get sumission failed: ", json["message"]);
        }
        else
        {
            let info = json["data"];
            setResult(id, info["result"], info["result_msg"], info);
            window.clearInterval(timerDict[id]);
        }
    })
    .fail(function (xhr, status, err) {
        console.error(`Error: ${err}`);
        console.error(`Status: ${status}`);
        console.dir(xhr);
    })
    .always(function (xhr, status) {
    });
}

$(document).ready(function () {
    let rejudgeBtns = $('button[name="rejudge"]').click(function () {
        let id = $(this).attr('id').replace(/rejudge-/, '');
        // Send rejudge info
        $.ajax({
            type: "GET",
            url: $(this).val(),
            dataType: "json"
        })
            .done(function (json) {
                // console.log(json);
                // loading
                $(`#${id}-result`).empty(); // preserve the old info?
                $(`#${id}-result`).append(`<div class="spinner-border text-success" style="width: 1.5rem; height: 1.5rem;" role="status">`);

                $(`#${id}-memory`).text("--");
                $(`#${id}-runtime`).text("--");
                // Set timer for checking result
                timerDict[id] = window.setInterval(function () {
                    checkResult(id);
                }, 1000);
            })
            .fail(function (xhr, status, err) {
                console.error(`Error: ${err}`);
                console.error(`Status: ${status}`);
                console.dir(xhr);
            })
            .always(function (xhr, status) {
            });
    });
});
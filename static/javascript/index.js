$(document).ready(function() {
    // Add more expertise fields
    $('#add-expertise').click(function() {
        $('#expertise-container').append(`
            <input type="text" class="texpertise">
        `);
    });
});


function addtrainer() {
    const tname = $("#tname").val();
    const tdesc = $("#tdesc").val();
    const tbio = $("#tbio").val();
    const texperience = $("#texperience").val();
    const user_id = $("#user_id").val();
    const tspec = $("#tspec").val();
    const timg = $("#timg")[0].files[0];
     if(!tspec){
        $("#tspec").css('border-color','red')
        return;
    }
    else if(!timg){
        $("#timg").css('border-color','red')
        return;
    }

    const formdata = new FormData();
    formdata.append("tname", tname);
    formdata.append("tdesc", tdesc);
    formdata.append("tbio", tbio);
    formdata.append("tspec", tspec);
    formdata.append("user_id", user_id);
    const expertiseArray = [];
    $(".texpertise").each(function() {
        expertiseArray.push($(this).val());
    });
    formdata.append("texpertise", JSON.stringify(expertiseArray)); 
    formdata.append("texperience", texperience);
    formdata.append("timg", timg);
    
    $.ajax({
        type: "POST",
        url: "/add_trainer/",
        data: formdata,
        processData: false,
        contentType: false,
        success: function(data) {
            if (data['status'] == 'pass') {
                $("#message").text('Trainer Added Successfully').css('color','#28a475')
                setTimeout(() => {
                    window.location.reload()
                }, 2000);
            } else if(data['status'] == 'fail') {
                $("#message").text(data['message']).css('color','#dc3545')
                $("#tname").css('border-color','red')
            }
        },
    });
}

$(document).ready(function() {
    // Trigger filtering when region is changed
    $("#fregion").change(filterBy);
    
    // Optionally, trigger filtering when the date is selected/changed
    $("#fdate").on("input", filterBy);
});

function filterBy(){
    let fregion = $("#fregion").val();
    let fdate = $("#fdate").val();

    if (fregion) { // Only proceed if a region is selected
        $.ajax({
            type: "POST",
            url: "/filter_by/",
            data: {
                "fregion": fregion,
                "fdate": fdate,
                "csrfmiddlewaretoken": "{{ csrf_token }}",  // Include CSRF token if needed
            },
            success: function(data){
                alert("Filtered Successfully");
                // Display data on the page as needed
                console.log(data); // View data for debugging
            },
            error: function(xhr, status, error){
                console.error("Error:", error);
            }
        });
    }
}
function OpenCourse(id) { 
    window.location.href = '/course/'+encodeURIComponent(id)
 }
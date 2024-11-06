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
function trainerDetails(id) { 
    window.location.href = '/view_trainer/'+encodeURIComponent(id)
 }
function Jobs() { 
    window.location.href = "/post_job"
 }

 function jobs(id){
    window.location.href = '/job/'+encodeURIComponent(id)+'/'
}
$(document).ready(function() {
    const YOUR_APP_ID = "9a012741";
    const YOUR_APP_KEY = "62640d675bd28172f530f7f4d7a792a6";

    $.ajax({
        type: "GET",
        url: `http://api.adzuna.com/v1/api/jobs/gb/categories?app_id=${YOUR_APP_ID}&app_key=${YOUR_APP_KEY}&content-type=application/json`,
        success: function(response) {
            console.log(response); // Inspect the response
            const categories = response.results; // Access the results array
            if (Array.isArray(categories)) {
                categories.forEach(function(category) {
                    $('#job-categories').append(`
                        <a href="#" id="${category.tag}" class="flex items-center rounded-lg border border-gray-200 bg-white px-4 py-2 hover:bg-gray-50 dark:border-gray-700 dark:bg-gray-800 dark:hover:bg-gray-700">
                            <svg class="me-2 h-4 w-4 shrink-0 text-gray-900 dark:text-white" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="none" viewBox="0 0 24 24">
                                <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v5m-3 0h6M4 11h16M5 15h14a1 1 0 0 0 1-1V5a1 1 0 0 0-1-1H5a1 1 0 0 0-1 1v9a1 1 0 0 0 1 1Z"></path>
                            </svg>
                            <span class="text-sm font-medium text-gray-900 dark:text-white">${category.label}</span>
                        </a>
                    `);
                });
            } else {
                console.error("Categories not found or not an array in response");
            }
        },
        error: function(xhr, status, error) {
            console.error("Failed to fetch categories:", error);
        }
    });
});

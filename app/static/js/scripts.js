//Import tagify objects for event listeners     
import { fieldTagify, softwareTagify,
        addFieldTagify, addSoftwareTagify,
        fieldInWhitelist, softwareInWhitelist } from "./tags.js";

import {header, siteMenus, footer, footerMenus, universalMenus} from "https://esm.sh/@access-ci/ui@0.2.0"

const siteItems =[
    {
        name: "Report an Issue",
        href: "/"
    },
    {
        name: "Software Discovery Service",
        href: "/"
    }
]

$(document).ready(function(){
    $('html,body').animate({scrollTop:0},'fast')

    universalMenus({
        loginUrl: "/login",
        logoutUrl: "/logout",
        siteName: "Allocations",
        target: document.getElementById("universal-menus"),
    });
    header({
        siteName: "Support",
        target: document.getElementById("header")
    });
    siteMenus({
        items: siteItems,
        siteName: "Allocations",
        target: document.getElementById("site-menus"),
      });

    footerMenus({
        items: siteItems,
        target: document.getElementById("footer-menus"),
    });
    footer({ target: document.getElementById("footer") });
    
    //event listeners for tagify fields
    addFieldTagify.on("invalid", fieldInWhitelist)

    //softwareTagify.on("invalid", showAddSoftware);
    addSoftwareTagify.on("invalid", softwareInWhitelist);

    //initialize tooltips
    $('[data-toggle="tooltip"]').tooltip()

    // calculate scores when the form is submitted
    var formDataObject = {};
    $("#submit-form").on("click", function(){
        var form = document.getElementById("recommendation-form")
        let formIsValid = validateForm() 
        if (formIsValid){
            let formData = get_form_data(form);
            calculate_score(formData).then(function(recommendation){
                if (!(recommendation === "{}")){
                    display_score(recommendation);
                    // Creates the boxes for the top 3 recommendations in the modal
                    visualize_recommendations(recommendation, 3);
                    openModal(recommendation);
                    $("#see_less").hide()
                    // Saves the form data so that it can be used in the "See More" button below.
                    formDataObject = formData
                }else{
                    let alertMsg = "Not enough information to make recommendation. Please provide a more detailed response"
                    showAlert(alertMsg)
                }
            }).catch(function(error){
                console.log("error when calculating score: ", error)
            })
        }
        else
        {
            let alertMsg = "Please fill out all of the required fields"
            showAlert(alertMsg)
        }
        return false
    })

    //add three more calculated scores when see more button is clicked
    $('#see_more').on('click', function(){
        // load the form data from the original submition
        let formData = formDataObject
        // Reads the number of boxes/recommendations in the modal to only load the subsequent three
        var numberOfBoxes = $("#modal-body .box").length;
        calculate_score(formData).then(function(recommendation){
                
            if (!(recommendation === "{}")){
                // Makes the next three boxes/recommendations and adds to the modal  
                visualize_recommendations(recommendation, numberOfBoxes+3)
                .then(() => {
                })
                .catch((error) => {
                    console.error("Error occurred: " + error);
                    // Hide the "See More" button and show the "See Less" when all recommendations have been displayed
                    $("#see_more").hide()
                    $("#see_less").show()   
                });       
            }   
            }).catch(function(error){
                console.log("error when calculating score: ", error)
            })
        })    
        
    // Reduce the recommendations back down to the top three
    $('#see_less').on('click', function(){
        // load the form data from the original submition
        let formData = formDataObject
        // Clears the modal
        document.querySelector('.modal-body').innerHTML = '';
        //Calculates the top three and displays them in the modal
        calculate_score(formData).then(function(recommendation){
            if (!(recommendation === "{}")){
                visualize_recommendations(recommendation, 3);
                $("#see_more").show()
                $("#see_less").hide()
                }
    })
})

    //Show RPs if user has experience
    $('input[name="hpc-use"]').change(function() {
        if ($(this).val() === '1') {
          $('.hide-hpc').removeClass('d-none').show();
        } else {
          $('.hide-hpc').addClass('d-none').hide();
        }
      });

    //Show GUI checkboxes if user needs GUI
    $('input[name="gui-needed"]').change(function(){
        if ($(this).val() === '1'){
            $('.hide-gui').removeClass('d-none').show();
        } else {
            $('.hide-gui').addClass('d-none').hide();
        }
    });

    //Show storage questions if user needs storage
    $('input[name="storage"]').change(function() {
        if ($(this).val() === '1') {
          $('.hide-data').removeClass('d-none').show();
        } else if ($(this).val() === '2') {
           $('.hide-data').removeClass('d-none').show(); 
        } else {
            $('.hide-data').addClass('d-none').hide();
        }
      });

    $("#submitModal").on('hidden.bs.modal',function(e){
        $(".modal-body").empty();

    })

    // Clear the form
    $("#clear-form").on('click',function(){
        let form = document.getElementById("recommendation-form");
        form.reset();
    })
    $("#clear-form-modal").on('click',function(){
        let form = document.getElementById("recommendation-form");
        form.reset();
    })
    

});

function showAlert(alertMsg){
    $("#alert-div").append(
        `<div class="alert alert-danger alert-dismissible fade show" id="alert" role="alert">
            ${alertMsg}
            <button type="button" class="close" data-dismiss="alert" aria-label="Close">
                <span aria-hidden="true">&times;</span>
            </button>
        </div>`
    )
    $("#alert").fadeTo(2000, 500).slideUp(1000, function(){
        $("#alert").slideUp(1000);
        $("#alert").alert('close')
    });
    $('html,body').animate({scrollTop:0},'fast')
}

function validateForm() {
    var valid = 1;

    //Find elements based on required attribute
    var reqFields = $("[required]")

    reqFields.each(function(){
        //Find name for those elements
        var name = $(this).attr("name");

        //Find values from those names if name exists, otherwise
        //directly check value. If value on required question is
        //undefined, set valid to 0 and display error message.
        if (name){
            if ($(`input[name=${name}]:checked`).val() == undefined){
                valid = 0;
                $(`[name=${name}]`).addClass("is-invalid")
            }else{
                $(`[name=${name}]`).removeClass("is-invalid")
            }
         }else{
            if (!$(this).val()){
                valid = 0;
                $(this).addClass("is-invalid")
            }else{
                $(this).removeClass("is-invalid")
            }
        }
    });

    return valid;
}

function display_score(score){
    $("#rpScore").append(
        $(`
            <label class="form-check-label text-wrap" for=""> 
                ${score}
            </label>`
        )
        )
}

function get_form_data(form){
    let formData = new FormData(form)

    //Set research field tags and added tags
    let fieldTagValues = fieldTagify.value.map(tag => tag.value)
    formData.set('research-field', fieldTagValues)
    let fieldAddTags = addFieldTagify.value.map(tag => tag.value)
    formData.set('add-field-tags', fieldAddTags)

    //Set software tags and added tags
    let softwareTagValues = softwareTagify.value.map(tag => tag.value)
    formData.set('software', softwareTagValues)
    let softwareAddTags = addSoftwareTagify.value.map(tag => tag.value)
    formData.set('add-software-tags', softwareAddTags)

    return formData
}

function calculate_score(formData){

    // get and process data from each input field
    let jsonData = {}
    formData.forEach(function(value,key){
        if (key == "used-hpc" || key == "used-gui"){
            if (!jsonData[key]) {
                jsonData[key] = [value];
            } else {
                jsonData[key].push(value);
            }
        } else {
            jsonData[key]=value
        }
    });

    //calculating score from backend
    return new Promise(function(resolve,reject){
        $.ajax({
            type:"POST",
            url:"/get_score",
            data:JSON.stringify(jsonData),
            contentType:"application/json",
            success:function(recommendation){
                resolve(recommendation)
            },
            error:function(error){
                reject(error)
            }
        });
    }); 
       
}

//function to parse JSON data a create a boxes in the modal to display them
async function visualize_recommendations(scores, recNum){
    // parses JSON data from calculate scores function
    var parsedScores = JSON.parse(scores);
    var recommendations=[];
    //Creates a variable recommendations that houses the parsed JSON data
    for (var rp in parsedScores) {
        if (parsedScores.hasOwnProperty(rp)) {
            var score = parsedScores[rp]['score'];
            var reasons = parsedScores[rp]['reasons'];
            recommendations.push({ name: rp, score: score, reasons: reasons });
        }
    }
    // sorts the recommendations from high to low scores
    recommendations.sort(function(a, b) {
        return b.score - a.score;
    });
    // takes recNum argument to make params that only display a certain section of recommendations. Used for "See More" button
    var low = recNum-3
    var high = recNum
    for (let i=low; i<(high); i++){
        //Make a box to hold all of the info for each RP
        var box = document.createElement('div');
        box.classList.add('box');
        box.id = `box${i}`;
        box.innerHTML = box.innerHTML +`
            <div class="box-content" id='box${i}-content'>
            <h3 class="box-title" id="box${i}-name">${recommendations[i].name}</h3>
            <div class="tags-container" id="box${i}-suitability">
            <h4 class="tags-title"></h4>
            </div>
            <div class="body-container" id="box${i}-body"></div>
            </div>
            <span class="caret"><i class="fas fa-caret-down"></i></span>
            `;
        var body = document.querySelector('.modal-body')
        // Add the recommendation box to the modal body
        body.appendChild(box);

        //Generate "reason" tags for inside the boxes. These tags are the reasons for the recommendation
        var tagsContainer = document.getElementById(`box${i}-suitability`);
        if (tagsContainer) {
            var tags = recommendations[i].reasons;
            // creates the individual reason rtags
            if (tags) {
                tags.forEach(function(tag) {
                var tagElement = document.createElement('div');
                tagElement.classList.add('tag');
                tagElement.textContent = tag;
                tagsContainer.appendChild(tagElement);
                });
            }
        }
        
        //Generates blurbs and links for each RP by pulling from database
        try {
            // Make the AJAX request to info/blurb database using fetch API and await the response
            const jsonData = { rp: recommendations[i].name }; 
            const response = await $.ajax({    
                type: "POST",
                url: '/get_info',
                data: JSON.stringify(jsonData),
                contentType: "application/json",
                error:function(error){
                    reject(error)
                }
            });
            // takes the JSON response and uses it to add the blurbs and links into the recommendations boxes
            const info = await response;
            const bodyContainer = document.getElementById(`box${i}-body`);
            if (bodyContainer) {
                const blurbArray = info.blurb;
                const hyperlinkArray = info.hyperlink;
                const documentationArray = info.documentation;
                const index = info.rp.indexOf(recommendations[i].name);
                bodyContainer.innerHTML = bodyContainer.innerHTML + `
                    <p class="box-text">${blurbArray[index]}</p>
                    <a class="box-link" href="${hyperlinkArray[index]}" target="_blank">Brief Summary</a>
                    <a class="box-link" href="${documentationArray[index]}" target="_blank">Detailed Information</a>
                `;
            }
          } catch (error) {
            // Handle any other errors that might occur during the AJAX request
            console.error("Error fetching RP information:", error);
          }
    }
}
//function to show modal upon clicking submit button
function openModal() {
    $("#submitModal").modal("show");
}
// Waits for the user to click on a modal box and expands/shrinks upon click. Height is relative to the length of the info inside the body
document.querySelector('.modal-body').addEventListener('click', function(event) {
    var target = event.target;
    var box = target.closest('.box');
    if (box) {
        var content = box.querySelector('.body-container');
        var tags = box.querySelector('.tags-container');
        // If the box is already open
        if (box.style.maxHeight){
            box.style.maxHeight = null;
            box.classList.toggle('expand');
        }
        // If the box is not already open
        else{
            var textHeight = content.clientHeight;
            var tagHeight = tags.clientHeight;
            box.style.maxHeight = (parseInt(textHeight) + parseInt(tagHeight) + 90 + "px");
            box.classList.toggle('expand');
        }
    }
})
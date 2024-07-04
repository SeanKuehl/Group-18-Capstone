
function CopyText() {
    
    var textTitle = document.getElementById('PostTitle').innerText
    var textFeatures = document.getElementById('DataAndTags').innerText
    var textBody = document.getElementById('PostBody').textContent
    var entirePost = textTitle.concat("  Date and tags: ", textFeatures, " Post ", textBody);
        
    
    // Create a dummy input to copy the string array inside it
    var dummy = document.createElement("input");

    // Add it to the document
    document.body.appendChild(dummy);

    // Set its ID
    dummy.setAttribute("id", "dummy_id");

    // Output the array into it
    document.getElementById("dummy_id").value=entirePost;

    // Select it
    dummy.select();

    // Copy its contents
    //document.execCommand("copy");
    
    navigator.clipboard.writeText(dummy.value);

    // Remove it as its not needed anymore
    document.body.removeChild(dummy);
    
    
  }
 
function openTab(evt, tabName) {
        var i, tabContent, tabBtn;

        // Hide all tab content
        tabContent = document.getElementsByClassName("tab-content");
        for (i = 0; i < tabContent.length; i++) {
            tabContent[i].style.display = "none";
        }

        // Remove the 'active' class from all tab buttons
        tabBtn = document.getElementsByClassName("tab-btn");
        for (i = 0; i < tabBtn.length; i++) {
            tabBtn[i].className = tabBtn[i].className.replace(" active", "");
        }

        // Show the clicked tab content and set the 'active' class for the clicked tab button
        document.getElementById(tabName).style.display = "block";
        evt.currentTarget.className += " active";

    }
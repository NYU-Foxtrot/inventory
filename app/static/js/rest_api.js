$(function () {

    // ****************************************
    //  U T I L I T Y   F U N C T I O N S
    // ****************************************

    // Updates the form with data from the response
    function update_form_data(res) {
        $("#inventory_id").val(res.id);
        $("#inventory_name").val(res.name);
        $("#inventory_quantity").val(res.quantity.toString());
        $("#inventory_status").val(res.status);
    }

    /// Clears all form fields
    function clear_form_data() {
        $("#inventory_name").val("");
        $("#inventory_quantity").val("");
        $("#inventory_status").val("");
    }

    // Updates the flash message area
    function flash_message(message) {
        $("#flash_message").empty();
        $("#flash_message").append(message);
    }

    // ****************************************
    // Create a inventory
    // ****************************************

    $("#create-btn").click(function () {

        var name = $("#inventory_name").val();
        var quantity = parseInt($("#inventory_quantity").val());
        var status = $("#inventory_status").val();

        var data = {
            "name": name,
            "quantity": quantity,
            "status": status
        };

        var ajax = $.ajax({
            type: "POST",
            url: "/inventories",
            contentType:"application/json",
            data: JSON.stringify(data),
        });

        ajax.done(function(res){
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });
    });


    // ****************************************
    // Update a inventory
    // ****************************************

    $("#update-btn").click(function () {

        var inventory_id = $("#inventory_id").val();
        var name = $("#inventory_name").val();
        var quantity = parseInt($("#inventory_quantity").val());
        var status = $("#inventory_status").val();

        var data = {
            "name": name,
            "quantity": quantity,
            "status": status
        };

        var ajax = $.ajax({
                type: "PUT",
                url: "/inventories/" + inventory_id,
                contentType:"application/json",
                data: JSON.stringify(data)
            })

        ajax.done(function(res){
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });

    });

    // ****************************************
    // Retrieve a inventory
    // ****************************************

    $("#retrieve-btn").click(function () {

        var inventory_id = $("#inventory_id").val();

        var ajax = $.ajax({
            type: "GET",
            url: "/inventories/" + inventory_id,
            contentType:"application/json",
            data: ''
        })

        ajax.done(function(res){
            //alert(res.toSource())
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            clear_form_data()
            flash_message(res.responseJSON.message)
        });

    });

    // ****************************************
    // Delete a inventory
    // ****************************************

    $("#delete-btn").click(function () {

        var inventory_id = $("#inventory_id").val();

        var ajax = $.ajax({
            type: "DELETE",
            url: "/inventories/" + inventory_id,
            contentType:"application/json",
            data: '',
        })

        ajax.done(function(res){
            clear_form_data()
            flash_message("inventory with ID [" + inventory_id + "] has been Deleted!")
        });

        ajax.fail(function(res){
            flash_message("Server error!")
        });
    });

    // ****************************************
    // Clear the form
    // ****************************************

    $("#clear-btn").click(function () {
        $("#inventory_id").val("");
        clear_form_data()
    });

    // ****************************************
    // Search for a inventory
    // ****************************************

    $("#search-btn").click(function () {

        var name = $("#inventory_name").val();
        var quantity = $("#inventory_quantity").val();
        var status = $("#inventory_status").val();

        var queryString = ""

        if (name) {
            queryString += 'name=' + name
        }
        if (quantity) {
            if (queryString.length > 0) {
                queryString += '&quantity=' + quantity
            } else {
                queryString += 'quantity=' + quantity
            }
        }
        if (status) {
            if (queryString.length > 0) {
                queryString += '&status=' + status
            } else {
                queryString += 'status=' + status
            }
        }

        var ajax = $.ajax({
            type: "GET",
            url: "/inventories?" + queryString,
            contentType:"application/json",
            data: ''
        })

        ajax.done(function(res){
            //alert(res.toSource())
            $("#search_results").empty();
            $("#search_results").append('<table class="table-striped">');
            var header = '<tr>'
            header += '<th style="width:10%">ID</th>'
            header += '<th style="width:40%">Name</th>'
            header += '<th style="width:40%">Quantity</th>'
            header += '<th style="width:10%">status</th></tr>'
            $("#search_results").append(header);
            for(var i = 0; i < res.length; i++) {
                inventory = res[i];
                var row = "<tr><td>"+inventory.id+"</td><td>"+inventory.name+"</td><td>"+inventory.quantity+"</td><td>"+inventory.status+"</td></tr>";
                $("#search_results").append(row);
            }

            $("#search_results").append('</table>');

            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });

    });

    // ****************************************
    // List all inventories
    // ****************************************

    $("#list-btn").click(function () {

        var ajax = $.ajax({
            type: "GET",
            url: "/inventories",
            contentType:"application/json",
            data: ''
        })

        ajax.done(function(res){
            //alert(res.toSource())
            $("#search_results").empty();
            $("#search_results").append('<table class="table-striped">');
            var header = '<tr>'
            header += '<th style="width:10%">ID</th>'
            header += '<th style="width:40%">Name</th>'
            header += '<th style="width:40%">Quantity</th>'
            header += '<th style="width:10%">status</th></tr>'
            $("#search_results").append(header);
            for(var i = 0; i < res.length; i++) {
                inventory = res[i];
                var row = "<tr><td>"+inventory.id+"</td><td>"+inventory.name+"</td><td>"+inventory.quantity+"</td><td>"+inventory.status+"</td></tr>";
                $("#search_results").append(row);
            }

            $("#search_results").append('</table>');

            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });

    });

    // ****************************************
    // Query the quantity of an inventory
    // ****************************************

    $("#query-btn").click(function () {

        var name = $("#inventory_name").val();
        var quantity = $("#inventory_quantity").val();
        var status = $("#inventory_status").val();

        var queryString = ""

        if (name) {
            queryString += 'name=' + name
        }
        if (status) {
            if (queryString.length > 0) {
                queryString += '&status=' + status
            } else {
                queryString += 'status=' + status
            }
        }

        var ajax = $.ajax({
            type: "GET",
            url: "/inventories/query?" + queryString,
            contentType:"application/json",
            data: ''
        })

        ajax.done(function(res){
            //alert(res.toSource())
            $("#search_results").empty();
            $("#search_results").append('<table class="table-striped">');
            var header = '<tr>'
            header += '<th style="width:10%">ID</th>'
            header += '<th style="width:40%">Name</th>'
            header += '<th style="width:40%">Quantity</th>'
            header += '<th style="width:10%">status</th></tr>'
            $("#search_results").append(header);
            for(var i = 0; i < res.length; i++) {
                inventory = res[i];
                var row = "<tr><td>"+inventory.id+"</td><td>"+inventory.name+"</td><td>"+inventory.quantity+"</td><td>"+inventory.status+"</td></tr>";
                $("#search_results").append(row);
            }

            $("#search_results").append('</table>');

            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });

    });

})
Date.prototype.addDays=function(d){return new Date(this.valueOf()+864E5*d);};
document.getElementById('start_time').value = 8
document.getElementById('end_time').value = 24

function formatDate(date) {
    var d = new Date(date),
        month = '' + (d.getMonth() + 1),
        day = '' + d.getDate(),
        year = d.getFullYear();

    if (month.length < 2) 
        month = '0' + month;
    if (day.length < 2) 
        day = '0' + day;
    console.log(date)
    let weekday = String(date).substring(0, 3)
    switch (String(date).substring(0, 3)) {
        case "Mon": weekday = "Mo";break;
        case "Tue": weekday = "Di";break;
        case "Wed": weekday = "Mi";break;
        case "Thu": weekday = "Do";break;
        case "Fri": weekday = "Fr";break;
        case "Sat": weekday = "Sa";break;
        case "Sun": weekday = "So";break;
    }

    return [[weekday, day, month, year].join('-'), [year, month, day].join('')];
}

var currentState = {'day': "", 'layers': [], 'time': []}

date = new Date();
console.log(formatDate(date))

for (let i = 0; i < 7; i++) {
    var button = document.createElement('button');
    button.temp = formatDate(date.addDays(i))
    button.innerHTML = button.temp[0];
    button.status = false;
    button.day = i
    button.onclick = function(){
        if (this.status) {
            this.status = false
            this.style.background = '#812a2a'
            
        } else {
            this.status = true
            this.style.background = '#56bb6c'
            currentState.day = this.temp[1];
        }
    };
    document.getElementById('days').appendChild(button);
}

const layers = ['eg', 'og_1', 'og_2_ost', 'og_2_mitte', 'og_2_west', 'og_3_ost', 'og_3_mitte', 'og_3_west', 'og_4']
const layers_pretty = ['Ebene 0', 'Ebene 1', 'Ebene 2 Ost', 'Ebene 2 Mitte', 'Ebene 2 West', 'Ebene 3 Ost', 'Ebene 3 Mitte', 'Ebene 3 West', 'Ebene 4']

for (let i = 0; i < 9; i++) {
    var button = document.createElement('button');
    button.innerHTML = layers_pretty[i];
    button.status = false;
    button.layer = layers[i]
    button.onclick = function(){
        if (this.status) {
            this.status = false
            this.style.background = '#812a2a'
            const index = currentState.layers.indexOf(layers[i]);
            if (index > -1) {
                currentState.layers.splice(index, 1);
            }
        } else {
            this.status = true
            this.style.background = '#56bb6c'
            currentState.layers.push(layers[i])
        }
    };
    document.getElementById('layer').appendChild(button);
}

function get_seats() {
    currentState.time = [document.getElementById('start_time').value, document.getElementById('end_time').value]

    if(currentState.day == "" || currentState.layers.length == 0) {
        return
    }
    
    $.ajax({
        type: "POST",
        url: "find_seats",
        contentType: "application/json;charset=UTF-8",
        data: JSON.stringify(currentState),
        dataType: "json",
        success: function(response) {
            console.log(response);
        },
        error: function(err) {
            console.log(err);
        }
    });
}
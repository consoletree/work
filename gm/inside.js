function takeattendace() {
        var total = Number(document.getElementsByClassName('uGOf1d')[0].textContent);
        const names = []

        for (let i=0; i<total; i++){
                names.push(document.getElementsByClassName('ZjFb7c')[i].textContent);
        }
        console.log("its done");
}

function download() {
        let a = document.createElement('a');
        a.href = "data:application/octet-stream,"+encodeURIComponent(names);
        a.download = 'attendace.txt';
        a.click();
        console.log("downloaded");
}


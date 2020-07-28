// let {PythonShell} = require('python-shell');

// let options = {
//     mode: 'text',
//     pythonPath: 'path/to/python',
//     pythonOptions: ['-u'], // get print results in real-time
//     scriptPath: 'path/to/my/scripts',
//     args: ['value1', 'value2', 'value3']
//   };

// PythonShell.run('flipkart.py',null, function (err, results){
//     if (err) throw err;
//     console.log('finished');
// })

const spawn = require('child_process').spawn;

const process = spawn('python',['./main.py']);

process.stdout.on('data', data =>{
    console.log(data.toString());
})





function taskStatusDTO(task){
    return {
        status: task.Status
    }
}

function createdTaskDTO(taskId){
    return {
        taksid: taskId
    }
}

exports.taskStatusDTO = taskStatusDTO;
exports.createdTaskDTO = createdTaskDTO;
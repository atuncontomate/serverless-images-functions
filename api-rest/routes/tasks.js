const express = require ('express');
const dtoMappers = require('../dto/dtoMappers');

const tasksRepository = require('../repository/tasksRepository');
const uploadService = require('../service/uploadService')

const router = express.Router();
const multer  = require('multer')
const upload = multer();

router.post('/', upload.any(), async (req, res) => {

    const files = req.files;
    if(!(files)) {
        res.sendStatus(400);
    } else {
        const savedTaskId = await Promise.all(files.map(async image => {
            const filepath = await uploadService.uploadImageToResize(image);
            return await tasksRepository.save(filepath);
        }));
        res.json(dtoMappers.createdTaskDTO(savedTaskId[0]))
    }

});

router.get('/:id', async (req, res) => {
    const id = req.params.id;
    const task = await tasksRepository.findById(id);

    if (task) {
        res.json(dtoMappers.taskStatusDTO(task))
    } else {
        res.sendStatus(404);
    }
});

module.exports = router;
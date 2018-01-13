import axios from 'axios';

const root = 'http://localhost:8080';

export function getData(url) {
    return new Promise((resolve, reject) => {
        axios.get(`${root}/${url}`)
            .then(res => {
                resolve(res.data);
            })
            .catch(err => {
                reject(err);
            });
    });
}

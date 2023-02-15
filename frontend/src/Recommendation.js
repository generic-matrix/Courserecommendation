const HOST = "http://192.168.43.250:5001"

async function Recommendation(query) {
    return new Promise(async(resolve, reject) => {
        console.log(HOST+'/recommend?query='+query)
        const response = await fetch(HOST+'/recommend?query='+query, {
        method: 'GET',
            headers: {
                Accept: 'application/json',
                'Content-Type': 'application/json',
            },
        });
        response.json().then((res)=>{
            resolve(res)
        }).catch((error)=>{
            reject(error)
        })
    });
}

async function Autocomplete(query) {
    return new Promise(async(resolve, reject) => {
        const response = await fetch(HOST+'/autocomplete?query='+query, {
        method: 'GET',
        headers: {
            Accept: 'application/json',
            'Content-Type': 'application/json',
        },
        });
        response.json().then((res)=>{
            resolve(res)
        }).catch((error)=>{
            reject(error)
        })
    });
}

export default {
    "Autocomplete":Autocomplete,
    "Recommendation":Recommendation
};
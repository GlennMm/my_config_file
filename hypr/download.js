const https = require('https')
const fs = require('fs')

const links = [
    'hypr-catppuccin/waybar/config',
    'hypr-catppuccin/waybar/modules',
    'hypr-catppuccin/waybar/style.css'
]

links.forEach(url => {

    https.get(`https://raw.githubusercontent.com/eldermf/bspwm-hyprland/master/hyprland/home/.config/${url}`, async (res) => {

        const arr = url.split('/')
        arr.reverse()
        
        if (!fs.existsSync(`${__dirname}/${arr[1]}`)) {
            fs.mkdirSync(`${__dirname}/${arr[1]}`)
        }
        
        const path = `${__dirname}/${arr[1]}/${arr[0]}`


        const filePath = fs.createWriteStream(path)
        res.pipe(filePath)
        filePath.on('finish', ()=>{
            filePath.close()
            console.log(`${arr[1]}/${arr[0]} Downloaded.`)
            // console.log(`${arr[2]}/${arr[1]}/${arr[0]} Downloaded.`)
        })

    })

})



import * as THREE from 'three';
import { FBXLoader } from '/static/js/FBXLoader.js';
import { GLTFLoader } from '/static/js/GLTFLoader.js';
import { OrbitControls } from '/static/js//OrbitControls.js';
import Stats from '/static/js/stats.module.js';
import { Scene } from '/static/js//three.module.js';
import {MeshPhongMaterial} from '/static/js//MeshPhongMaterial.js';
import * as dat from 'https://cdn.jsdelivr.net/npm/dat.gui@0.7.9/build/dat.gui.module.js';
import {BoxGeometry, DoubleSide, Mesh, MeshBasicMaterial, PMREMGenerator, TextureLoader} from "three";

//init

let stats, mixer, canvas, canvasWidth, canvasHeight, clock;
let camera, scene, renderer, controls, group;
let loadModel, tempModel, action;

// "/static/new_model/agegroup"
let basic_model_path = "";
let currentSelection = "/model1/";
let cloth = true;
let hair = true;

//skin, hair, top, bottom
let femaleTextureCombination = ["Body_00, (path)_10.png,Face_00, (path)_04.png", "Hair_00, (path)_16.png,HairBack, (path)_12.png", "Tops, (path)_15.png", "Bottoms, (path)_13.png"];
let maleTextureCombination = ["Body_00, (path)_10.png,Face_00, (path)_04.png", "Hair_00, (path)_17.png", "Tops_01, (path)_14.png,Tops_02, (path)_15.png,Tie, (path)_16.png", "Bottoms, (path)_13.png"];


//test version for model under /static/model/test2/ folder only
init("canvas");

function sceneInit(canvasID) {
        //canvas set up
        canvas = document.getElementById(canvasID);
        //document.body.appendChild(canvas);
        canvasWidth = document.getElementById(canvasID).clientWidth;
        canvasHeight = document.getElementById(canvasID).clientHeight;

        clock = new THREE.Clock();

        //set up camera
        camera = new THREE.PerspectiveCamera( 30, canvasWidth / canvasHeight, 0.1, 10000);
        //camera.position.set(1.66,2.05,3.61);
        camera.position.set(1.4485807979862497,2.0668476949423362,3.934246459224377);
        //camera.rotation.set(-0.34, 0.51, 0.17);
        camera.lookAt(0,1,-1);
        //console.log(camera);

        //scene set up, background color debug use only
        scene = new THREE.Scene();
        scene.background = new THREE.Color(0xD6E7C5);
        
        //set up render
        renderer = new THREE.WebGLRenderer( {antialias: true, alpha: true } );
        renderer.setSize( canvasWidth , canvasHeight );
        document.body.appendChild( renderer.domElement );
        renderer.setPixelRatio( window.devicePixelRatio );
        renderer.shadowMap.enabled = true;
        renderer.toneMapping = THREE.ACESFilmicToneMapping;
        renderer.toneMappingExposure = 1;
        canvas.appendChild(renderer.domElement);


        //light
        const light = new THREE.AmbientLight(0xffffff,0.8);
        light.position.set(10.0, 10.0, 10.0).normalize();
        //light.castShadow = true;
        scene.add(light);
        var light2 = new THREE.DirectionalLight(0xffffff,1);
        light2.position.set(0, 3, 2);
        light2.castShadow = true;
        scene.add(light2);
        var light3 = new THREE.DirectionalLight(0xffffff,1);
        light3.position.set(0, 0, 2);
        light3.castShadow = true;
        scene.add(light3);


        //grid
        // const gridHelper = new THREE.GridHelper(10, 10);
        // gridHelper.receiveShadow = true;
        // scene.add(gridHelper);

        // //Skybox ((( COMPLETE BUT NOT IN FINAL PRODUCT )))
        // let textureLoader = new TextureLoader();
        // let skyBoxGeometry = new BoxGeometry(40, 40, 40);
        // //the textures pattern in skybox material is left, right, up, down, front, back, px, nx, py, ny, pz, nz
        // //current scene: 13, 14_b, 20, 21, 23_b
        // let skyBoxMaterial = [
        //     new MeshBasicMaterial({ map: textureLoader.load('./static/background/png/20/px.png'), side: DoubleSide}),
        //     new MeshBasicMaterial({ map: textureLoader.load('./static/background/png/20/nx.png'), side: DoubleSide}),
        //     new MeshBasicMaterial({ map: textureLoader.load('./static/background/png/20/py.png'), side: DoubleSide}),
        //     new MeshBasicMaterial({ map: textureLoader.load('./static/background/png/20/ny.png'), side: DoubleSide}),
        //     new MeshBasicMaterial({ map: textureLoader.load('./static/background/png/20/pz.png'), side: DoubleSide}),
        //     new MeshBasicMaterial({ map: textureLoader.load('./static/background/png/20/nz.png'), side: DoubleSide})
        // ];
        // let skyboxMesh = new Mesh(skyBoxGeometry, skyBoxMaterial);
        // skyboxMesh.position.set(0, -3, 0);
        // scene.add(skyboxMesh);

        //set up stats
        // stats = new Stats();
        // document.body.appendChild( stats.dom );

        //set up controller(enable user to control camera)
        controls = new OrbitControls(camera, renderer.domElement)
        controls.enableDamping = true
        controls.target.set(0, 1, 0)
        controls.update()
}
async function reload(canvasID){
    scene.remove(loadModel);

    //Async loader!
    const fbxLoader = new FBXLoader().setPath( basic_model_path + currentSelection);
    [loadModel, tempModel] = await Promise.all( [
        fbxLoader.loadAsync( 'Idle.fbx' ),
        fbxLoader.loadAsync( 'Idle.fbx' )
    ] );

    setTexture();
    var hair_colour = document.getElementsByName("hair_colour");
    for(var i=0;i<hair_colour.length;i++){
        if(hair_colour[i].checked){readInput(hair_colour[i].value);}
    }
     var top = document.getElementsByName("top");
    for(var i=0;i<top.length;i++){
        if(top[i].checked){readInput(top[i].value);}
    }
     var bot = document.getElementsByName("bot");
    for(var i=0;i<bot.length;i++){
        if(bot[i].checked){readInput(bot[i].value);}
    }
     var skin_colour = document.getElementsByName("skin_colour");
    for(var i=0;i<skin_colour.length;i++){
        if(skin_colour[i].checked){readInput(skin_colour[i].value);}
    }


//    var input = document.getElementById("hair_colour_1").value;
//    readInput(input);
//    var input = document.getElementById("top_1").value;
//    readInput(input);
//    var input = document.getElementById("bot_1").value;
//    readInput(input);
//    var input = document.getElementById("skin_colour_1").value;
//    readInput(input);

    loadModel.traverse( child => {

        if (child instanceof THREE.Mesh) {
            child.material.transparent = true;
            child.material.side = THREE.DoubleSide;
            child.material.alphaTest = 0.5;
        }
    })
    scene.add(loadModel);
    loadModel.position.set(0,0.25,0);
    setFbxAnimation(loadModel);


}
async function init(canvasID) {

    // group = new THREE.Group();
    sceneInit(canvasID);
    basic_model_path =  "/static/new_model/" + document.getElementById("model_age_group").innerText;

    //Async loader!
    const fbxLoader = new FBXLoader().setPath( basic_model_path + currentSelection);
    [loadModel, tempModel] = await Promise.all( [
        fbxLoader.loadAsync( 'Idle.fbx' ),
        fbxLoader.loadAsync( 'Idle.fbx' )
    ] );



    


    setTexture();

    var input = document.getElementById("hair_colour_1").value;
    readInput(input);
    var input = document.getElementById("top_1").value;
    readInput(input);
    var input = document.getElementById("bot_1").value;
    readInput(input);
    var input = document.getElementById("skin_colour_1").value;
    readInput(input);

    loadModel.traverse( child => {

        if (child instanceof THREE.Mesh) {
            child.material.transparent = true;
            child.material.side = THREE.DoubleSide;
            child.material.alphaTest = 0.5;
        }
    })

    scene.add(loadModel);
    //new stage
    const stageLoader = new FBXLoader().setPath("/static/model/test/");
    var [stage] = await Promise.all([
        stageLoader.loadAsync("Podium.fbx")
    ]);
    var list = []
    for (var i = 0; i < stage.children.length;i++) {
        if (stage.children[i].name != "Camera"
        &&stage.children[i].name != "Light" &&
        stage.children[i].name != "Light002"
        ) {
            list.push(stage.children[i]);
        }

    }
    stage.children = list;
    scene.add(stage);

    scene.traverse(child =>{
        if (child instanceof THREE.Mesh) {
            child.frustumCulled = false;
        }
    })
    stage.scale.multiplyScalar(0.004);
    
    // console.log(loadModel);
    // console.log(loadModel.position);
    loadModel.position.set(0,0.25,0);
    //loadVrmModel.translateY(1.0);
    console.log(stage)

    //end stage
    setFbxAnimation(loadModel);
    
}

function setFbxAnimation(model) {
    //animation
    mixer = new THREE.AnimationMixer( model );
    action = mixer.clipAction( model.animations[ 0 ] );
    action.play();
    animate();
}


function animate() {
    requestAnimationFrame( animate );
    const delta = clock.getDelta();
    if ( mixer ) mixer.update( delta );
    renderer.render( scene, camera );
    //console.log(camera.position);
    //stats.update();
}


function TextureChange(targetTextureName, newTexturePath) {
    loadModel.traverse( child => {
        if (child instanceof THREE.Mesh) {

            if (child.name.indexOf(targetTextureName) != -1) {

                let newTexture = new THREE.TextureLoader().load(newTexturePath);
                child.material.map = newTexture;
                child.material.needsUpdate = true;

            }
        }
    })
}

function readInput(input){
    input = input.split(",");
    for (let i = 0; i < input.length; i+=2) {
        TextureChange(input[i], input[i+1]);
    }
}


function setTexture(){
    let skin1, skin2, skin3;
    let hair1, hair2, hair3;
    let top1, top2, top3;
    let bottom1, bottom2, bottom3;

    if(basic_model_path.indexOf("_female") != -1){
        skin1 = femaleTextureCombination[0].replaceAll('(path)', basic_model_path + currentSelection + "option1_texture/");
        skin2 = femaleTextureCombination[0].replaceAll('(path)', basic_model_path + currentSelection + "option2_texture/");
        skin3 = femaleTextureCombination[0].replaceAll('(path)', basic_model_path + currentSelection + "option3_texture/");
        hair1 = femaleTextureCombination[1].replaceAll('(path)', basic_model_path + currentSelection + "option1_texture/");
        hair2 = femaleTextureCombination[1].replaceAll('(path)', basic_model_path + currentSelection + "option2_texture/");
        hair3 = femaleTextureCombination[1].replaceAll('(path)', basic_model_path + currentSelection + "option3_texture/");
        top1 = femaleTextureCombination[2].replaceAll('(path)', basic_model_path + currentSelection + "option1_texture/");
        top2 = femaleTextureCombination[2].replaceAll('(path)', basic_model_path + currentSelection + "option2_texture/");
        top3 = femaleTextureCombination[2].replaceAll('(path)', basic_model_path + currentSelection + "option3_texture/");
        bottom1 = femaleTextureCombination[3].replaceAll('(path)', basic_model_path + currentSelection + "option1_texture/");
        bottom2 = femaleTextureCombination[3].replaceAll('(path)', basic_model_path + currentSelection + "option2_texture/");
        bottom3 = femaleTextureCombination[3].replaceAll('(path)', basic_model_path + currentSelection + "option3_texture/");
    }else if(basic_model_path.indexOf("_male") != -1){
        skin1 = maleTextureCombination[0].replaceAll('(path)', basic_model_path + currentSelection + "option1_texture/");
        skin2 = maleTextureCombination[0].replaceAll('(path)', basic_model_path + currentSelection + "option2_texture/");
        skin3 = maleTextureCombination[0].replaceAll('(path)', basic_model_path + currentSelection + "option3_texture/");
        hair1 = maleTextureCombination[1].replaceAll('(path)', basic_model_path + currentSelection + "option1_texture/");
        hair2 = maleTextureCombination[1].replaceAll('(path)', basic_model_path + currentSelection + "option2_texture/");
        hair3 = maleTextureCombination[1].replaceAll('(path)', basic_model_path + currentSelection + "option3_texture/");
        top1 = maleTextureCombination[2].replaceAll('(path)', basic_model_path + currentSelection + "option1_texture/");
        top2 = maleTextureCombination[2].replaceAll('(path)', basic_model_path + currentSelection + "option2_texture/");
        top3 = maleTextureCombination[2].replaceAll('(path)', basic_model_path + currentSelection + "option3_texture/");
        bottom1 = maleTextureCombination[3].replaceAll('(path)', basic_model_path + currentSelection + "option1_texture/");
        bottom2 = maleTextureCombination[3].replaceAll('(path)', basic_model_path + currentSelection + "option2_texture/");
        bottom3 = maleTextureCombination[3].replaceAll('(path)', basic_model_path + currentSelection + "option3_texture/");
    }

    document.getElementById("skin_colour_1").value = skin1;
    document.getElementById("skin_colour_2").value = skin2;
    document.getElementById("skin_colour_3").value = skin3;
    document.getElementById("hair_colour_1").value = hair1;
    document.getElementById("hair_colour_2").value = hair2;
    document.getElementById("hair_colour_3").value = hair3;
    document.getElementById("top_1").value = top1;
    document.getElementById("top_2").value = top2;
    document.getElementById("top_3").value = top3;
    document.getElementById("bot_1").value = bottom1;
    document.getElementById("bot_2").value = bottom2;
    document.getElementById("bot_3").value = bottom3;
    document.getElementById("clothing_style_1").value = basic_model_path+currentSelection;
    document.getElementById("clothing_style_2").value = basic_model_path+currentSelection;
    document.getElementById("hair_style_1").value = basic_model_path+currentSelection;
    document.getElementById("hair_style_2").value = basic_model_path+currentSelection;
}
/* Model change */
 document.getElementById("clothing_style_1").onclick = function clothing_style_1(){
    cloth = true;
    if(hair){currentSelection = "/model1/";}
    else{currentSelection = "/model2/";}
    reload("canvas");
 }

 document.getElementById("clothing_style_2").onclick = function clothing_style_2(){
    cloth = false;
    if(hair){currentSelection = "/model3/";}
    else{currentSelection = "/model4/";}
    reload("canvas");
 }

 document.getElementById("hair_style_1").onclick = function hair_style_1(){
    hair = true;
    if(cloth){currentSelection = "/model1/";}
    else{currentSelection = "/model3/";}
    reload("canvas");
 }

 document.getElementById("hair_style_2").onclick = function hair_style_2(){
    hair = false;
    if(cloth){currentSelection = "/model2/";}
    else{currentSelection = "/model4/";}
    reload("canvas");
 }

/* Model hair colour change */
document.getElementById("hair_colour_1").onclick = function hair_colour_1(){
    var input = document.getElementById("hair_colour_1").value;
    readInput(input);
}
document.getElementById("hair_colour_2").onclick = function hair_colour_2(){
    var input = document.getElementById("hair_colour_2").value;
    readInput(input);
}

document.getElementById("hair_colour_3").onclick = function hair_colour_3(){
    var input = document.getElementById("hair_colour_3").value;
    readInput(input);
}

/* Model top dress change */
document.getElementById("top_1").onclick = function top_1(){
    var input = document.getElementById("top_1").value;
    readInput(input);
}

document.getElementById("top_2").onclick = function top_2(){
    var input = document.getElementById("top_2").value;
    readInput(input);
}

document.getElementById("top_3").onclick = function top_3(){
    var input = document.getElementById("top_3").value;
    readInput(input);
}

/* Model bottom dress change */
document.getElementById("bot_1").onclick = function bot_1(){
    var input = document.getElementById("bot_1").value;
    readInput(input);
}

document.getElementById("bot_2").onclick = function bot_2(){
    var input = document.getElementById("bot_2").value;
    readInput(input);
}

document.getElementById("bot_3").onclick = function bot_3(){
    var input = document.getElementById("bot_3").value;
    readInput(input);
}

/* Model skin colour change */
document.getElementById("skin_colour_1").onclick = function skin_colour_1(){
    var input = document.getElementById("skin_colour_1").value;
    readInput(input);
}

document.getElementById("skin_colour_2").onclick = function skin_colour_2(){
    var input = document.getElementById("skin_colour_2").value;
    readInput(input);
}

document.getElementById("skin_colour_3").onclick = function skin_colour_3(){
    var input = document.getElementById("skin_colour_3").value;
    readInput(input);
}



let vrmModel, vrmTempModel, currentVrm;
async function loadVrmModel(canvasID,localPath) {

    const loader = new THREE.GLTFLoader();

    loader.register((parser) => {return new THREE_VRM.VRMLoaderPlugin( parser, {autoUpdateHumanBones: true } );}); // here we are installing VRMLoaderPlugin
    [vrmModel, vrmTempModel] = await Promise.all(
        [
            loader.loadAsync(localPath),
            loader.loadAsync(localPath)
        ]
    )
    
    const oriVrm = vrmModel.userData.vrm
    const targetVrm = vrmTempModel.userData.vrm
    //scene.add(oriVrm.scene);
    //scene.remove(vrm.scene);
    currentVrm = oriVrm;
    //loadFBX( currentAnimationUrl );
}
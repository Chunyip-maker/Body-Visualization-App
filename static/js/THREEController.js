import * as THREE from 'three';
import { FBXLoader } from '/static/js/FBXLoader.js';
import { OrbitControls } from '/static/js//OrbitControls.js';
import Stats from '/static/js/stats.module.js';
import { Scene } from '/static/js//three.module.js';
import {MeshPhongMaterial} from '/static/js//MeshPhongMaterial.js';
import * as dat from 'https://cdn.jsdelivr.net/npm/dat.gui@0.7.9/build/dat.gui.module.js';

//init

let stats, mixer, canvas, canvasWidth, canvasHeight, clock;
let camera, scene, renderer, controls, group;
let loadModel, tempModel, action;


//test version for model under /static/model/test2/ folder only
init("canvas", "Breathing Idle2.fbx");



async function init(canvasID, modelName) {

    //canvas set up
    canvas = document.getElementById(canvasID);
    //document.body.appendChild(canvas);
    canvasWidth = document.getElementById(canvasID).clientWidth;
    canvasHeight = document.getElementById(canvasID).clientHeight;


    //GUI debug only, will remove later
    let gui = new dat.GUI();
    console.log("init run");
    const background_1 = {
    "color": 0xffffff
    };

    
    clock = new THREE.Clock();

    //set up camera
    camera = new THREE.PerspectiveCamera( 30, canvasWidth / canvasHeight, 0.1, 20);
    camera.position.set(1.66,2.05,3.61);
    //camera.rotation.set(-0.34, 0.51, 0.17);
    camera.lookAt(0,1,0);
    console.log(camera);


    //scene set up, background color debug use only
    scene = new THREE.Scene();
    scene.background = new THREE.Color(background_1.color);
    
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
    const gridHelper = new THREE.GridHelper(10, 10);
    gridHelper.receiveShadow = true;
    scene.add(gridHelper);


    //set up stats
    stats = new Stats();
    document.body.appendChild( stats.dom );

            //set up controller(enable user to control camera)
    controls = new OrbitControls(camera, renderer.domElement)
    controls.enableDamping = true
    controls.target.set(0, 1, 0)
    controls.update()


    //fbx loader
    let boneMenu = [];
    let objectCopy = null;
    let modelObject;


    group = new THREE.Group();
    scene.add(group);


    //background color menu, debug only
    let displayFolder = gui.addFolder("Display");
    const material = new MeshPhongMaterial();
    displayFolder.addColor(background_1, "color").onChange((color) => {
        scene.background = new THREE.Color(background_1.color);
    });


    //Async loader!
    const fbxLoader = new FBXLoader().setPath( '/static/model/test2/' );
    [loadModel, tempModel] = await Promise.all( [
        fbxLoader.loadAsync( 'Breathing Idle2.fbx' ),
        fbxLoader.loadAsync( 'Breathing Idle2.fbx' )
    ] );


    //animation
    group.add(loadModel);
    console.log(loadModel.children);
    mixer = new THREE.AnimationMixer( loadModel );
    action = mixer.clipAction( loadModel.animations[ 0 ] );
    action.play();
    //end animation

    //debug use, should be called after the init finished.
    //all gui in this part will be remove later
    //current gui for debug only
    loadModel.traverse( child => {

        if (child.type == "Bone") {
                
                if ( !boneMenu.includes(child.name) && child.name.indexOf("J_Sec") == -1) {
                    let boneFolder = gui.addFolder(child.name);
                    boneFolder.add(child.scale, 'x',0.8, 1.2).name("Scale" + " X");
                    boneFolder.add(child.scale, 'y',0.8, 1.2).name("Scale" + " Y");
                    boneFolder.add(child.scale, 'z',0.8, 1.2).name("Scale" + " Z");
                    boneFolder.add(child.position, 'x',0, 3).name("position" + " X");
                    boneFolder.add(child.position, 'y',0, 3).name("position" + " Y");
                    boneFolder.add(child.position, 'z',0, 3).name("position" + " Z");
                    console.log(child.name);
                    console.log(child);
                }

                boneMenu.push(child.name);
            }

        if (child instanceof THREE.Mesh) {


            child.material.transparent = true;
            child.material.side = THREE.DoubleSide;
            child.material.alphaTest = 0.5;
            console.log(child.name);
            

            if (child.name == "N00_001_01_Bottoms_01_CLOTH_(Instance)") {

                
                let temp = "/static/model/old_male/model1/Old Male.vrm.textures/_12.png"
                const bottom = ["1","2","3",temp];

                gui.add({ bottom: bottom[0]}, "bottom")
                .options(bottom)
                .onChange((val) => {
                    var newTexture = new THREE.TextureLoader().load(val);
                    child.material.map = newTexture;
                    child.material.needsUpdate = true;
                });

            }

            if (child.name == "N00_001_01_Bottoms_01_CLOTH_(Instance)") {

                
                let temp = "/static/model/old_male/model1/Old Male.vrm.textures/_12.png"
                const bottom = ["1","2","3",temp];

                gui.add({ bottom: bottom[0]}, "bottom")
                .options(bottom)
                .onChange((val) => {
                    var newTexture = new THREE.TextureLoader().load(val);
                    child.material.map = newTexture;
                    child.material.needsUpdate = true;
                });

            }

        }
        })
        animate();
}


function animate() {
    requestAnimationFrame( animate );
    const delta = clock.getDelta();
    if ( mixer ) mixer.update( delta );
    renderer.render( scene, camera );
    stats.update();

}


function TextureChange(targetTextureName, newTexturePath) {
    loadModel.traverse( child => {
        if (child instanceof THREE.Mesh) {
            
            if (child.name == targetTextureName) {

                var newTexture = new THREE.TextureLoader().load(newTexturePath);
                child.material.map = newTexture;
                child.material.needsUpdate = true;

            }
        }
    })
}






//API of modify bones

document.getElementById("a1").oninput = function changeHeight(){
    console.log("111");
    let value = document.getElementById("a1").value;
    document.getElementById("b1").innerText = value;

    loadModel.traverse( child => {

    })
}

document.getElementById("a2").oninput = function changeWeight(){
    console.log("111");
    let value = document.getElementById("a2").value;
    document.getElementById("b2").innerText = value;

    loadModel.traverse( child => {

    })
}


document.getElementById("a3").oninput = function changeChest(){
    console.log("111");
    let value = document.getElementById("a3").value;
    document.getElementById("b3").innerText = value;

    loadModel.traverse( child => {

    })
}

document.getElementById("a4").oninput = function changeWaist(){
    console.log("111");
    let value = document.getElementById("a4").value;
    document.getElementById("b4").innerText = value;

    loadModel.traverse( child => {

    })
}

document.getElementById("a5").oninput = function changeHip(){
    console.log("111");
    let value = document.getElementById("a5").value;
    document.getElementById("b5").innerText = value;

    loadModel.traverse( child => {

    })
}

document.getElementById("a6").oninput = function changeArm(){
    console.log("111");
    let value = document.getElementById("a6").value;
    document.getElementById("b6").innerText = value;

    loadModel.traverse( child => {

    })
}

document.getElementById("a7").oninput = function changeThigh(){
    console.log("111");
    let value = document.getElementById("a7").value;
    document.getElementById("b7").innerText = value;

    loadModel.traverse( child => {

    })
}

document.getElementById("a8").oninput = function changeShank(){
    console.log("111");
    let value = document.getElementById("a8").value;
    document.getElementById("b8").innerText = value;

    loadModel.traverse( child => {

    })
}


//clean texture, add gui, temp





//gui.hide();
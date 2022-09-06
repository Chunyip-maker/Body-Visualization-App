
import * as THREE from 'three';
import { FBXLoader } from './FBXLoader.js';
import { OrbitControls } from './OrbitControls.js';
import Stats from '/static/js/stats.module.js';
import { Scene } from './three.module.js';
import {MeshPhongMaterial} from './MeshPhongMaterial.js';
import * as dat from 'https://cdn.jsdelivr.net/npm/dat.gui@0.7.9/build/dat.gui.module.js';


class THREEController {

    scene;
    camera;
    mixer;
    spotlight;
    clock;
    renderer;
    stats;
    windowWidth;
    windowHeight;
    background_1 = {
        "color": 0x3e44ba
    };

    constructor() {
        this.windowWidth = window.innerWidth;
        this.windowHeight = window.innerHeight;
    }

    windowSize = () => {
        
    }

    animate = ()=>{
        requestAnimationFrame( this.animate );
        
        this.spotlight.position.set(
            this.camera.position.x + 10,
            this.camera.position.y + 10,
            this.camera.position.z + 10
        )

        const delta = this.clock.getDelta();
        if ( this.mixer ) this.mixer.update( delta );
        this.renderer.render( this.scene, this.camera );
        this.stats.update();

    }

    init = ()=> {
            //init

        //GUI not yet
        let gui = new dat.GUI();
        console.log("init run");
        // let stats, mixer;
        this.clock = new THREE.Clock();
                //set up camera
        this.camera = new THREE.PerspectiveCamera( 70, this.windowWidth / this.windowHeight, 0.01, 100);
        this.camera.position.set(0,2,3);


        //set up scene, with white background color
        this.scene = new THREE.Scene();
        this.scene.background = new THREE.Color(this.background_1.color);

        //general light
        var light = new THREE.HemisphereLight(0xffeeb1,0x080820,4);
        this.scene.add(light);

        //set up render
        this.renderer = new THREE.WebGLRenderer( { antialias: true } );
        //render for texture which need alpha pipe
        //const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true, premultipliedAlpha: true });
        this.renderer.setSize( this.windowWidth, this.windowHeight );
        document.body.appendChild( this.renderer.domElement );
        this.renderer.setPixelRatio( window.devicePixelRatio );
        //this.renderer.setAnimationLoop(this.animation);
        this.renderer.shadowMap.enabled = true;
        this.renderer.toneMapping = THREE.ReinhardToneMapping;
        this.renderer.toneMappingExposure = 2.3; 



        //spotlight
        this.spotlight = new THREE.SpotLight(0xffa95c, 4);
        this.spotlight.castShadow = true;
        this.scene.add( this.spotlight );

        //set up stats
        this.stats = new Stats();
        document.body.appendChild( this.stats.dom );


        //set up controller(enable user to control camera)
        const controls = new OrbitControls(this.camera, this.renderer.domElement)
        controls.enableDamping = true
        controls.target.set(0, 1, 0)



        const loadingManager = new THREE.LoadingManager();
        loadingManager.setURLModifier( ( url ) => {

            // this function is called for each asset request
            if (url.length > 100) {
                url = url.substring(69, 116);
                console.log(url);
            }
            //console.log(url);
            return url;

        } );

        //fbx loader
        let boneMenu = [];
        
        let modelObject;
        const loader = new FBXLoader(loadingManager);
        loader.load( '/static/model/test/Idle (11).fbx', ( object ) => {
                
                
                this.mixer = new THREE.AnimationMixer( object );

                const action = this.mixer.clipAction( object.animations[ 0 ] );
                action.play();


                let count = 0;
                object.traverse( ( child ) => {

                    if (child instanceof THREE.Mesh) {
                        child.material.transparent = true;
                        child.material.side = THREE.DoubleSide;
                        child.material.alphaTest = 0.3;
                        console.log(child.name);
                        

                        //Customization, dat gui

                        // var Facebrow = new THREE.TextureLoader().load("/static/model/test/testG.vrm.textures/_07.png");
                        // child.material.map = Facebrow;
                        // child.material.needsUpdate = true;

                    }

                    //add all bones to dat gui
                    if (child.type == "Bone") {
                        
                        //console.log(child.name);

                        //update gui
                        if ( !boneMenu.includes(child.name) ) {
                            let boneFolder = gui.addFolder(child.name);
                            boneFolder.add(child.scale, 'x',0, 2).name(child.name + " X");
                            boneFolder.add(child.scale, 'y',0, 2).name(child.name + " Y");
                            boneFolder.add(child.scale, 'z',0, 2).name(child.name + " Z");
                        }

                        boneMenu.push(child.name);
                    }
                    
                } );
                this.scene.add( object );
        } );

        
        // animation
        this.animate();


        //gui update
        let displayFolder = gui.addFolder("Display");
        const material = new MeshPhongMaterial();
        displayFolder.addColor(this.background_1, "color").onChange((color) => {
            this.scene.background = new THREE.Color(this.background_1.color);
        });

    
    }


};


export { THREEController };











/*
Idea about using morph target to change diff part of the model.
*/
//set up GLTF loader and texture

//const texture = new THREE.TextureLoader().load("/static/model/astronaut/textures/AStronoaut_Baked_baseColor.png");
// texture.flipY = false;
// texture.encoding = THREE.sRGBEncoding;

//load model file
// const loader = new GLTFLoader();
// let modelObject;
// let morphTargets = [];
// let tempVariable;
// loader.load('/static/model/test/ok.glb', (gltf) => {
//     modelObject = gltf.scene;

//     mixer = new THREE.AnimationMixer( modelObject );

//     const action = mixer.clipAction( gltf.animations[ 0 ] );
//     action.play();

//     modelObject.traverse((child) => {
//         if (child.isMesh) {
//             child.material.metalness = 0;
//             child.material.vertexColors = false;
//             child.castShadow = true;
//             child.receiveShadow = true;
            
//             //target the morph target
//             // if (child.morphTargetDictionary) {

//             //     morphTargets["helmets"] = [];
//             //     morphTargets["helmets"].push({ child });

//             // }
//         }
//         console.log(child.name);
//         if (child.type == "Bone") {
//                 //add gui
//                 if (child.name == "Left_leg86") {
                    
//                     gui.add(child.scale, 'x',0, 2).name("Left Leg");
//                     gui.add(child.scale, 'z',0, 2).name("Left Leg");
//                 }

//                 if (child.name == "Right_leg93") {
                
//                     gui.add(child.scale, 'x',0, 2).name("Right Leg");
//                     gui.add(child.scale, 'z',0, 2).name("Right Leg");
//                 }


//             }
//     });
//     console.log(morphTargets);
//     scene.add(modelObject);
// });

// console.log(morphTargets.length);

/*
end of morph example
*/


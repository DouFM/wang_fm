/*
*    module
*/
var fmApp = angular.module('FMApp', ['ngRoute', 'ngCookies', 'ngResource']);


/*
*   FMCtrl controller
*/
function FMCtrl($scope, $http, MusicList, Music, User) {
    angular.element(document).ready(function() {
        navInit();
        playerInit();
        $('ul.thumb li').Zoomer({speedView:200,speedRemove:400,altAnim:true,speedTitle:400,debug:false});
    });

    //navbar initial
    function navInit() {
        $scope.currentUser = User.get({arg: 'current/'}, function(data) {
            $scope.data = data;
            // console.log(data);
            if(data.name !== undefined) {
                var loginBar = '<a target="_blank" href="/static/app/views/personal.html">' + data.name + '</a>';
                var regBar = '<a href="#" onclick="logout()">退出</a>';
                $('#loginBar').html(loginBar);
                $('#regBar').html(regBar);

                if(data.level === 'admin') {
                    $('#gn-menu').append('<li id="mBar"><a target="_blank" href="/static/app/views/manager.html">管理</a></li><li style="border:0;"></li>');
                } 
            } 
        });
        // console.info($scope.currentUser);
    }

    //login logout and register
    $scope.login = function() {
        console.info('loign');
        var loginname = $('#login_name').val();
        var login_password = $('#login_password').val();
        var loginData = {
            arg: 'current/',
            name: loginname,
            password: login_password
            // password: 'wang1129'
        };
        var loginInfo = User.login(loginData, function(data) {
            var loginBar = '<a href="#">' + data.name + '</a>';
            $('#login').modal('hide');
            $('#loginBar').html(loginBar);
            var regBar = '<li><a href="#" onclick="logout()">退出</a></li>';
            $('#regBar').html(regBar);
            if(data.level === 'admin') {
                $('#gn-menu').append('<li id="mBar"><a  target="_blank" href="/static/app/views/manager.html">管理</a></li><li style="border:0;"></li>');
            }
        });
    } 

    $scope.reg = function() {
        console.info('register');
        var username = $("#username").val();
        var password = $("#password").val();
        var password2 = $("#password2").val();
        if (username === '' || password === '' || password2 === '' || (password !== password2)) {
            alert("please check your input");
        } else {
            var regData = {
                name: username,
                password: password 
            };
            console.log(regData);
            $http.post('/api/user/', regData).success(function (data) {
                console.log(data);
                var loginData = {
                    arg: 'current/',
                    name: username,
                    password: password
                };
                User.login(loginData, function(data) {
                    var loginBar = '<a href="#">' + data.name + '</a>';
                    $('#register').modal('hide');
                    $('#loginBar').html(loginBar);
                    var regBar = '<li><a href="#" onclick="logout()">退出</a></li>';
                    $('#regBar').html(regBar);
                });
            });    
        }
    }

    //music player 
    $scope.index = 0;
    function playerInit() {
        new jPlayerPlaylist({
            jPlayer: "#jquery_jplayer_1",
            cssSelectorAncestor: "#jp_container_1"
        }, 
        [],
        { 
            ready: playReady,
            ended: playEnded,
            swfPath: "/static/app/vender/jPlayer/js",
            supplied: "mp3",
            wmode: "window",
            smoothPlayBar: true,
            keyEnabled: true
        });

        // $("#jp-report").html('<a href="#" data-toggle="tooltip" data-placement="top" title="请注册后使用!" alt="report" ><img src="../images/report.png"></img></a>');
    }

    function playReady() {
        // console.info(" playReady ok");
        MusicList.query(function(data) {
            // console.info(data);
            $scope.musics = MusicList.query({arg: data[0].key, num: 10}, function(data) {
                // console.info(data[1]);
                playMusic(data[$scope.index]);
            });
        });
    };

    function playEnded() {
        // console.info('playEnded ok');
        $scope.index = $scope.index + 1;
        console.info($scope.index);
        if($scope.index == 10) {
            $scope.index = 0;
            playReady();
        } else {
            console.info('playMusic');
            playMusic($scope.musics[$scope.index]);
        }
    };

    function playMusic(musicArr){
        // console.info(musicArr);
        $("#jquery_jplayer_1").jPlayer("setMedia", { mp3: musicArr.audio }).jPlayer("load").jPlayer("play");
        $("#jp-cover img").attr("src",musicArr.cover);
        $("#jp-singer").html(musicArr.artist);
        $("#nameAlbum").html(musicArr.title + '     ' + musicArr.album);
    }

    //click next button in the music player
    $scope.clickNext = function() {
        $scope.index = $scope.index + 1;
        // console.info($scope.index);
        if($scope.index == 10) {
            $scope.index = 0;
            playReady();
        } else {
            // console.info('playMusic');
            playMusic($scope.musics[$scope.index]);
        }
    }

    //click cover in the recent 10 musics
    $scope.clickPlay = function(index) {
        // console.info(index);
        $scope.index = index;
        playMusic($scope.musics[index]);
    }

    //list for all users 
    $scope.lists = MusicList.query({start: 0});;
    $scope.playthis = function(key) {
        var listKey = key;
        $scope.index = 0;
        $scope.musics = MusicList.query({arg: key, num: 10}, function(data) {
            playMusic(data[0]);
        });
    }
}

function logout() {
    console.info('logout');
    $.ajax({
        type: 'delete',
        url: "/api/user/current/",
        success: function() {
            //console.info("logout");
            window.location.href = '/static/app/views/index.html';
        }
    });
}

/*
*   manager controller
*/
function managerCtrl($scope, $http, Music, Channel, User) {
    
    //music info display
    $scope.musics = Music.query({start: 0, end: 14});

    // channel info display
    $scope.channelNumAll = Channel.get();
    $scope.channels = Channel.query({start: 0, end: 14});

    //user info display
    $scope.users = User.query({start: 0});
}

/*
*   personal controller
*/
function personalCtrl($scope, $http, Music, User) {
    $scope.currentUser = User.get({arg: 'current/'});
}
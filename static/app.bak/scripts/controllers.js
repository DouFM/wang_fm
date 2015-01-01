/*
*    module
*/
var fmApp = angular.module('FMApp', ['ngRoute', 'ngResource']);

/*
*   主界面控制器
*/
function FMCtrl($scope, $http, MusicList, Music, User) {
    //DOM ready
    angular.element(document).ready(function() {      
        
        //分析当前url判断是首次进入或者是点击分享链接进入（分享链接进入会传入参数key）
        (function analysisUrl () {
            //获取当前url中传入参数key，若为空则播放器进入正常初始化；
            //否则，进入分享模式初始化（当前暂时只有一个参数）。
            var url = window.location.href;
            var shareKey = url.split('=')[1];
            if (shareKey === undefined) {
                Player.listInit();
            } else {
                Player.init(Player.shareReady(shareKey), Player.shareEnded);
            }
        })();

        //navbar initial
        (function navInit() {
            $scope.currentUser = User.get({arg: 'current/'}, function(data) {
                $scope.data = data;
                // console.log(data);
                if(data.name !== undefined) {
                    var loginBar = '<a target="_blank" href="/static/app/views/personal.html">' + data.name + '</a>';
                    var regBar = '<a href="#"  onclick="logout()">退 出</a>';
                    $('#loginBar').html(loginBar);
                    $('#regBar').html(regBar);

                    if(data.level === 'admin') {
                        $('#regBar').before('<li id="mBar"><a target="_blank" href="/static/app/views/manager.html">管 理</a></li>');
                    } 
                } 
            });
        })();
        
        $('ul.thumb li').Zoomer({speedView:200,speedRemove:400,altAnim:true,speedTitle:400,debug:false});
    });

    //musicPlayer
    var Player = (function () {
        /* return object*/
        var playerObj = {};

        var randTenIndex = 0;   //判断随机取得十首歌是否播放完毕
        var defaultKey = '';    //正常模式进入默认播放歌曲分类key

        playerObj.listInit = function () {
            //获取所有歌曲分类列表，并且把第一个列表的key赋给$scope.defaultKey（默认播放的列表key）
            $scope.lists = MusicList.query(function(data) {
                // console.log(data);
                defaultKey = data[0].key;
                console.log(defaultKey);
                $scope.currentChannel = data[0].name;
                Player.init(Player.playerReady, Player.playerEnded);
            });
        }

        playerObj.init = function (funcR, funcE) {
            // console.log('init');
            new jPlayerPlaylist({
                jPlayer: "#jquery_jplayer_1",
                cssSelectorAncestor: "#jp_container_1"
            }, 
            [],
            { 
                ready: funcR,
                ended: funcE,
                swfPath: "/static/app/vender/jPlayer/js",
                supplied: "mp3",
                wmode: "window",
                smoothPlayBar: true,
                keyEnabled: true
            });        

            $scope.currentUser = User.get({arg: 'current/'}, function(data) {
                $scope.data = data;
                console.log(data);
                if(data.name !== undefined) {
                    $http.get('/api/user/current/favor/', {'start' : 0, 'end' : 10}).success(function (data) {
                        console.log(data);
                    });
                } 
            });
            
            //复制分享信息到剪切板
            $('#jp-shared').zclip({
                path: '/static/app/vender/ZeroClipboard.swf',
                copy: function(){
                    return $scope.shareMsg.replace(/\<br \/\>/g, '\r\n');
                },
                afterCopy: function (){
                    $('#share').modal('hide');
                }
            });
        }

        playerObj.playerReady = function () {
            // console.log('ready');
            //获取分类列表集合
            MusicList.query(function(data) {
                // console.log(data);
                //随机获取默认分类十首歌曲，并开始播放
                $scope.musics = MusicList.query({arg: defaultKey + '/', num: 10}, function(data) {
                    // console.log(data);
                    playMusic(data[randTenIndex]);
                });
            });
        }
        playerObj.playerEnded = function  () {
            console.log('ended');
            randTenIndex +=  1;
            // console.info(randTenIndex);
            if(randTenIndex == 10) {
                //如果十首歌曲播放完毕，调用playerReady()重新加载十首歌曲播放
                randTenIndex = 0;
                playerReady();
            } else {
                // console.info('playMusic');
                //否则继续播放下一首歌曲
                playMusic($scope.musics[randTenIndex]);
            }
        }

        //分享歌曲准备播放
        playerObj.shareReady = function (shareKey) {
            // console.log(shareKey);
            //根据分享可取key获取歌曲对象
            Music.query({key: shareKey}, function(data) {
                // console.log(data);
                playMusic(data[0]);
                $('#recentTenSongs').css('display', 'none');
                $('#gn-menu li:first-child').css('display', 'none');
                var homeUrl = 'http://' + window.location.host;
                // console.log(homeUrl);
                $('#currentChannel').html('<a href="' + homeUrl + '">去主页瞧瞧~</a>').css('padding-left', '145px');
            });
        }

        //分享歌曲播放完毕，弹出提示框
        playerObj.shareEnded = function () {
            console.log('scope');
            $('#shareEnd').modal('show');
        }

        /* private function*/
        //播放歌曲，musicObj为歌曲对象
        function playMusic(musicObj){
            // console.info(musicObj);
            var currentUrl = window.location.host;
            $scope.shareMsg = '很好听的一首歌，快来听吧!<br />' + musicObj.artist + '--' + musicObj.title + "<br />http://" + currentUrl + '/#key=' + musicObj.key ;
            $('#shareMsg').html($scope.shareMsg);
            $("#jquery_jplayer_1").jPlayer("setMedia", { mp3: musicObj.audio }).jPlayer("load").jPlayer("play");
            $("#jp-cover img").attr("src",musicObj.cover);
            $("#jp-singer").html(musicObj.artist);
            $("#nameAlbum").html(musicObj.title + '     ' + musicObj.album);
        }

        //点击播放下一首歌曲
        $scope.clickNext = function() {
            randTenIndex = randTenIndex + 1;
            // console.info($scope.index);
            if(randTenIndex == 10) {
                //如果十首歌曲播放完毕，调用playerReady()重新加载十首歌曲播放
                randTenIndex = 0;
                playerReady();
            } else {
                //否则继续播放下一首歌曲
                playMusic($scope.musics[randTenIndex]);
            }
        }

        //点击随机选取多十首歌曲封面，播放歌曲
        $scope.clickCover = function(index) {
            // console.info(index);
            randTenIndex = index;
            playMusic($scope.musics[index]);
        }

         //点击分类列表，随机播放该类十首歌曲
        $scope.clickList = function(key, name) {
            // var listKey = key;
            defaultKey = key;
            $scope.currentChannel = name;
            //置randTenIndex为0，随机获取新分类十首歌曲
            randTenIndex = 0;
            $scope.musics = MusicList.query({arg: defaultKey + '/', num: 10}, function(data) {
                playMusic(data[0]);
            });
        }

        // trash button 
        $scope.dislike = function () {
            console.log('dislike');
            var trashSrc = ['/static/app/images/trash2.png', '/static/app/images/trash.png'];
            var postData = {
                'op': 'dislike',
                'key': defaultKey
            };
            var jpTrash = $('jp-trash img');
            if (true) {
            };
            $http.post('/api/user/current/history/', postData).success(function (data) {
                var jpTrash = $('#jp-trash img');
                jpTrash.attr('src', trashSrc[1]);
            });
        }

        // favorite button
        $scope.like = function () {
           
            var favorSrc = ['/static/app/images/favorote2.png', '/static/app/images/favorite.png'];
            var postData = {
                'op': 'favor',
                'key': defaultKey
            };
            $http.post('/api/user/current/history/', postData).success(function (data) {
                console.log('like');
                var jpFavor = $('#jp-favorite img');
                jpFavor.attr('src', favorSrc[1]);
            });
        }
        return playerObj;
    })();

    //user 
    var Users = (function () {
        var userObj = {};
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
                var regBar = '<li><a href="#" onclick="logout()">退 出</a></li>';
                $('#regBar').html(regBar);
                if(data.level === 'admin') {
                    $('#currentChannel').before('<li id="mBar"><a target="_blank" href="/static/app/views/manager.html">管理</a></li>');
                }
            });
        } 

        $scope.reg = function () {
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
                    // console.log(data);
                    var loginData = {
                        arg: 'current/',
                        name: username,
                        password: password
                    };
                    User.login(loginData, function(data) {
                        var loginBar = '<a href="#">' + data.name + '</a>';
                        $('#register').modal('hide');
                        $('#loginBar').html(loginBar);
                        var regBar = '<li><a href="#" onclick="logout()">退 出</a></li>';
                        $('#regBar').html(regBar);
                    });
                });    
            }
        }

        window.logout = function () {
            console.info('logout');
            $.ajax({
                type: 'delete',
                url: "/api/user/current/",
                success: function() {
                    window.location.href = 'http://' + window.location.host;
                }
            });
        }
        return userObj;
    })();

    

}

/*
*   管理界面控制器
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
/*
 *    module
 */
var fmApp = angular.module('FMApp', []);

/*
 *   主界面控制器
 */
fmApp.controller("FMCtrl", function FMCtrl($scope, PlayList, ActivePlayList, UserHistory, UserMusic, Music, User) {

    //musicPlayer
    var Player = (function () {

        /* return object*/
        var playerObj = {};
        var musicNumber = 10; //每次请求的音乐数量
        var playMusicIndex = 0;  //当前播放的音乐索引
        var playListKey = '';  //当前播放列表的key

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

            //复制分享信息到剪切板
            $('#jp-shared').zclip({
                path: '/static/app/vender/ZeroClipboard.swf',
                copy: function () {
                    return $scope.shareMsg.replace(/\<br \/\>/g, '\r\n');
                },
                afterCopy: function () {
                    $('#share').modal('hide');
                }
            });

            //将player与Angular事件绑定
            bindEvent();
        };

        playerObj.nextMusic = function () {
            playMusicIndex = playMusicIndex + 1;
            if (playMusicIndex == $scope.musics.length) {
                playMusicIndex = 0;
                playerObj.playerReady();
            } else {
                playMusic($scope.musics[playMusicIndex]);
            }
        };

        //准备播放
        playerObj.playerReady = function () {
            PlayList.getArgs["num"] = musicNumber;
            PlayList.addUrlArg(playListKey);

            PlayList.get(
                function (data, status, headers, config) {
                    playMusicIndex = 0;
                    $scope.musics = data;
                    playMusic($scope.musics[playMusicIndex]);
                },
                function (data, status, headers, config) {
                }
            );
        };

        /* private function*/
        //播放歌曲，musicObj为歌曲对象
        function playMusic(musicObj) {

            var favorFlag = false;
            for (var i = 0; i < $scope.favorMusics.length; ++i) {
                if (musicObj.key == $scope.favorMusics[i].key) {
                    $scope.showFavor = true;
                    favorFlag = true;
                    break;
                }
            }
            if(!favorFlag){
                $scope.showFavor = false;
            }

            var currentUrl = window.location.host;
            $scope.shareMsg = '很好听的一首歌，快来听吧!<br />' + musicObj.artist + '--' + musicObj.title + "<br />http://" + currentUrl + '/#key=' + musicObj.key;
            $('#shareMsg').html($scope.shareMsg);
            $("#jquery_jplayer_1").jPlayer("setMedia", {mp3: musicObj.audio}).jPlayer("load").jPlayer("play");
            $("#jp-cover img").attr("src", musicObj.cover);
            $("#jp-singer").html(musicObj.artist);
            $("#nameAlbum").html(musicObj.title + '     ' + musicObj.album);
        }

        //获取用户相关的音乐
        $scope.getUserMusic = function (type, key, name, setListFlag) {
            UserMusic.getArgs["type"] = type;
            UserMusic.get(
                function (data, status, headers, config) {
                    if (data.length != 0) {
                        if(setListFlag){
                            playListKey = key;
                            $scope.currentChannel = name;
                            $scope.musics = data;
                            playMusicIndex = 0;
                            playMusic($scope.musics[0]);
                        }
                        if (type == "favor") {
                            $scope.favorMusics = data;
                        }
                        if (type == "listened") {
                            $scope.listenedMusics = data;
                        }
                    }
                },
                function (data, status, headers, config) {

                }
            );
        };


        //初始化播放列表
        playerObj.listInit = function () {
            $scope.favorMusics = [];
            $scope.listenedMusics = [];
            $scope.getUserMusic("favor", "favor", "喜欢", false);
            $scope.getUserMusic("listened", "listened", "听过", false);
            ActivePlayList.get(
                function (data, status, headers, config) {
                    $scope.lists = data;
                    playListKey = $scope.lists[0].key;
                    $scope.currentChannel = $scope.lists[0].name;
                    playerObj.init(playerObj.playerReady, playerObj.playerEnded);
                },
                function (data, status, headers, config) {

                }
            );

        };

        //分享歌曲准备播放
        playerObj.shareReady = function (shareKey) {
            // console.log(shareKey);
            //根据分享可取key获取歌曲对象
            Music.getArgs["key"] = shareKey;
            Music.get(
                function (data, status, headers, config) {
                    playMusic(data[0]);
                },
                function (data, status, headers, config) {
                }
            );

            $('#recentTenSongs').css('display', 'none');
            $('#gn-menu li:first-child').css('display', 'none');
            var homeUrl = 'http://' + window.location.host;
            // console.log(homeUrl);
            $('#currentChannel').html('<a href="' + homeUrl + '">去主页瞧瞧~</a>').css('padding-left', '145px');
        };


        //分享歌曲播放完毕，弹出提示框
        playerObj.shareEnded = function () {
            console.log('scope');
            $('#shareEnd').modal('show');
        };

        playerObj.nextMusic = function () {
            playMusicIndex = playMusicIndex + 1;
            if (playMusicIndex == $scope.musics.length) {
                playMusicIndex = 0;
                playerObj.playerReady();
            } else {
                playMusic($scope.musics[playMusicIndex]);
            }
        };

        //当前音乐播放完毕
        playerObj.playerEnded = function () {
            if (playListKey != "favor") {
                $scope.postHistory("listened", $scope.musics[playMusicIndex].key);
            }
            playerObj.nextMusic();
        };


        function bindEvent() {

            $scope.loginClick = function () {
                User.login();
            };

            $scope.logoutClick = function () {
                User.logout();
            };

            //发送history数据
            $scope.postHistory = function (type, musicKey) {
                UserHistory.postArgs["op"] = type;
                UserHistory.postArgs["key"] = musicKey;
                UserHistory.post(function (data, status, headers, config) {
                }, function (data, status, headers, config) {
                });
            };

            //点击下一曲歌曲
            $scope.clickNext = function () {
                playerObj.nextMusic();
            };


            //点击封面
            $scope.clickCover = function (index) {
                playMusicIndex = index;
                playMusic($scope.musics[index]);
            };


            //点击频道
            $scope.clickList = function (key, name) {
                playListKey = key;
                $scope.currentChannel = name;
                playMusicIndex = 0;
                playerObj.playerReady();
            };

            //点击收藏列表
            $scope.clickFavorList = function (key, name) {
                $scope.getUserMusic("favor", key, name, true);
            };

            //点击听过的音乐列表
            $scope.clickListenedList = function (key, name) {
                $scope.getUserMusic("listened", key, name, true);
            };

            //点击不喜欢按钮
            $scope.dislike = function () {
                $scope.postHistory("dislike", $scope.musics[playMusicIndex].key);
                playerObj.nextMusic();
            };

            //点击喜欢按钮
            $scope.like = function () {
                if ($scope.showFavor){
                    for (var i = 0; i < $scope.favorMusics.length; ++i) {
                        if ($scope.musics[playMusicIndex].key == $scope.favorMusics[i].key) {
                            $scope.favorMusics.splice(i, 1);
                            break;
                        }
                    }
                }
                else{
                    $scope.favorMusics.push($scope.musics[playMusicIndex]);
                }
                $scope.showFavor = !$scope.showFavor;
                $scope.postHistory("favor", $scope.musics[playMusicIndex].key);
            }
        }

        return playerObj;
    })();

    //DOM ready
    angular.element(document).ready(function () {
        //分析当前url判断是首次进入或者是点击分享链接进入（分享链接进入会传入参数key）
        (function analysisUrl() {
            //获取当前url中传入参数key，若为空则播放器进入正常初始化；
            //否则，进入分享模式初始化（当前暂时只有一个参数）。

            $scope.showFavor = false;

            var url = window.location.href;
            var shareKey = url.split('=')[1];
            if (shareKey === undefined) {
                Player.listInit();
            } else {
                Player.init(Player.shareReady(shareKey), Player.shareEnded);
            }
        })();

        $('ul.thumb li').Zoomer({speedView: 200, speedRemove: 400, altAnim: true, speedTitle: 400, debug: false});
    });
});
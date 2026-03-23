#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
小游戏系统 - 硅基世界 2

让 Agent 可以玩游戏娱乐。
"""

from datetime import datetime
from typing import Dict, List, Optional
from dataclasses import dataclass, field
from enum import Enum
import random


class GameType(Enum):
    """游戏类型"""
    PUZZLE = "puzzle"      # 益智
    CARD = "card"          # 卡牌
    BOARD = "board"        # 桌游
    SPORT = "sport"        # 运动
    ARCADE = "arcade"      # 街机


@dataclass
class Game:
    """游戏"""
    game_id: str
    name: str
    game_type: GameType
    description: str
    min_players: int = 1
    max_players: int = 4
    duration_minutes: int = 30
    
    def to_dict(self) -> Dict:
        return {
            "game_id": self.game_id,
            "name": self.name,
            "type": self.game_type.value,
            "description": self.description,
            "min_players": self.min_players,
            "max_players": self.max_players,
        }


@dataclass
class GameSession:
    """游戏会话"""
    session_id: str
    game: Game
    players: List[str]
    winner: Optional[str] = None
    started_at: Optional[float] = None
    ended_at: Optional[float] = None
    scores: Dict[str, int] = field(default_factory=dict)
    
    def to_dict(self) -> Dict:
        return {
            "session_id": self.session_id,
            "game": self.game.to_dict(),
            "players": self.players,
            "winner": self.winner,
            "scores": self.scores,
        }


class GameManager:
    """游戏管理器"""
    
    def __init__(self):
        """初始化游戏管理器"""
        self.games: Dict[str, Game] = {}
        self.sessions: Dict[str, GameSession] = {}
        self._game_counter = 0
        self._session_counter = 0
        
        # 玩家游戏统计
        self.player_stats: Dict[str, Dict] = {}
        
        # 注册游戏
        self._register_games()
        
        print("🎮 小游戏系统已初始化")
    
    def _register_games(self):
        """注册游戏"""
        games = [
            ("数独", GameType.PUZZLE, "经典数字益智游戏", 1, 1, 15),
            ("象棋", GameType.BOARD, "中国传统棋类游戏", 2, 2, 60),
            ("扑克", GameType.CARD, "经典纸牌游戏", 2, 4, 30),
            ("围棋", GameType.BOARD, "策略棋类游戏", 2, 2, 90),
            ("猜谜", GameType.PUZZLE, "猜谜语游戏", 1, 4, 10),
        ]
        
        for name, game_type, desc, min_p, max_p, duration in games:
            self._game_counter += 1
            self.games[f"game_{self._game_counter}"] = Game(
                game_id=f"game_{self._game_counter}",
                name=name,
                game_type=game_type,
                description=desc,
                min_players=min_p,
                max_players=max_p,
                duration_minutes=duration,
            )
    
    def create_session(
        self,
        game_id: str,
        players: List[str],
    ) -> Optional[GameSession]:
        """
        创建游戏会话
        
        Args:
            game_id: 游戏 ID
            players: 玩家列表
            
        Returns:
            游戏会话
        """
        if game_id not in self.games:
            return None
        
        game = self.games[game_id]
        
        if len(players) < game.min_players or len(players) > game.max_players:
            return None
        
        self._session_counter += 1
        
        session = GameSession(
            session_id=f"session_{self._session_counter}",
            game=game,
            players=players,
        )
        
        self.sessions[session.session_id] = session
        
        print(f"  🎮 开始游戏：{game.name} (玩家：{', '.join(players)})")
        
        return session
    
    def play_game(self, session_id: str) -> Optional[Dict]:
        """
        进行游戏
        
        Args:
            session_id: 会话 ID
            
        Returns:
            游戏结果
        """
        if session_id not in self.sessions:
            return None
        
        session = self.sessions[session_id]
        
        if session.started_at is not None:
            return None
        
        session.started_at = datetime.now().timestamp()
        
        # 模拟游戏结果
        scores = {}
        for player in session.players:
            scores[player] = random.randint(50, 100)
        
        session.scores = scores
        
        # 确定赢家
        winner = max(scores, key=scores.get)
        session.winner = winner
        session.ended_at = datetime.now().timestamp()
        
        # 更新玩家统计
        for player in session.players:
            if player not in self.player_stats:
                self.player_stats[player] = {
                    "games_played": 0,
                    "wins": 0,
                    "total_score": 0,
                }
            
            self.player_stats[player]["games_played"] += 1
            self.player_stats[player]["total_score"] += scores[player]
            
            if player == winner:
                self.player_stats[player]["wins"] += 1
        
        print(f"  🏆 {winner} 赢得了 {session.game.name}!")
        
        return {
            "winner": winner,
            "scores": scores,
        }
    
    def get_available_games(self) -> List[Game]:
        """获取可用游戏"""
        return list(self.games.values())
    
    def get_player_stats(self, player_id: str) -> Dict:
        """获取玩家统计"""
        return self.player_stats.get(player_id, {
            "games_played": 0,
            "wins": 0,
            "total_score": 0,
        })
    
    def get_leaderboard(self, limit: int = 10) -> List[Dict]:
        """获取游戏排行榜"""
        leaderboard = [
            {
                "player_id": player_id,
                "stats": stats,
                "win_rate": stats["wins"] / stats["games_played"] if stats["games_played"] > 0 else 0,
            }
            for player_id, stats in self.player_stats.items()
        ]
        
        leaderboard.sort(key=lambda x: x["win_rate"], reverse=True)
        
        return leaderboard[:limit]
    
    def get_stats(self) -> Dict:
        """获取统计信息"""
        return {
            "total_games": len(self.games),
            "total_sessions": len(self.sessions),
            "total_players": len(self.player_stats),
        }
    
    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            "stats": self.get_stats(),
            "games": [g.to_dict() for g in self.get_available_games()],
            "leaderboard": self.get_leaderboard(5),
        }


# 单例
_game_manager: Optional[GameManager] = None


def get_game_manager() -> GameManager:
    """获取游戏管理器单例"""
    global _game_manager
    if _game_manager is None:
        _game_manager = GameManager()
    return _game_manager


# 工厂函数
def create_game_manager() -> GameManager:
    """创建游戏管理器"""
    return GameManager()

-- ================================================================
-- Medical AI Chatbot Platform - Database Schema
-- 코드 분석을 통해 역산한 데이터베이스 스키마
-- ================================================================

-- ================================================================
-- 1. GLOBAL DATABASE (medichain_global)
-- ================================================================

CREATE DATABASE IF NOT EXISTS medichain_global;
USE medichain_global;

-- 사용자 기본 정보 테이블
CREATE TABLE users (
    user_id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL COMMENT '로그인 ID',
    email VARCHAR(100) DEFAULT '' COMMENT '이메일 (현재는 빈 문자열로 저장)',
    password_hash VARCHAR(64) NOT NULL COMMENT 'SHA256 해시값',
    salt VARCHAR(32) NOT NULL COMMENT '16바이트 hex salt',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    
    INDEX idx_username (username),
    INDEX idx_created_at (created_at)
);

-- 샤드 정보 테이블 (각 샤드 DB 연결 정보)
CREATE TABLE shard_info (
    shard_id INT PRIMARY KEY,
    host VARCHAR(255) NOT NULL COMMENT 'DB 호스트',
    port INT NOT NULL DEFAULT 3306 COMMENT 'DB 포트',
    database_name VARCHAR(100) NOT NULL COMMENT '샤드 DB명',
    username VARCHAR(100) NOT NULL COMMENT 'DB 사용자명',
    password VARCHAR(255) NOT NULL COMMENT 'DB 패스워드',
    is_active BOOLEAN DEFAULT TRUE COMMENT '활성 상태',
    max_connections INT DEFAULT 20 COMMENT '최대 연결 수',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    INDEX idx_active (is_active)
);

-- 사용자-샤드 매핑 테이블 (사용자가 어느 샤드에 속하는지)
CREATE TABLE user_shard_mapping (
    user_id INT PRIMARY KEY,
    shard_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (shard_id) REFERENCES shard_info(shard_id),
    INDEX idx_shard_id (shard_id)
);

-- ================================================================
-- 2. STORED PROCEDURES (Global Database)
-- ================================================================

DELIMITER //

-- 회원가입 + 샤드 할당을 원자적으로 처리하는 프로시저
CREATE PROCEDURE RegisterUser(
    IN p_username VARCHAR(50),
    IN p_email VARCHAR(100),
    IN p_password_hash VARCHAR(64),
    IN p_salt VARCHAR(32),
    IN p_shard_count INT
)
BEGIN
    DECLARE v_user_id INT;
    DECLARE v_shard_id INT;
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        RESIGNAL;
    END;
    
    START TRANSACTION;
    
    -- 1. 사용자 생성
    INSERT INTO users (username, email, password_hash, salt) 
    VALUES (p_username, p_email, p_password_hash, p_salt);
    
    SET v_user_id = LAST_INSERT_ID();
    
    -- 2. 샤드 할당 (라운드 로빈 방식: user_id % shard_count)
    SET v_shard_id = (v_user_id % p_shard_count);
    
    -- 3. 샤드 매핑 생성
    INSERT INTO user_shard_mapping (user_id, shard_id) 
    VALUES (v_user_id, v_shard_id);
    
    -- 4. 결과 반환 (account_template_impl.py에서 사용)
    SELECT v_user_id as user_id, v_shard_id as shard_id;
    
    COMMIT;
END //

DELIMITER ;

-- ================================================================
-- 2.5. SHARD DATABASE STORED PROCEDURES
-- ================================================================

DELIMITER //

-- 사용자별 채팅방 목록 조회 프로시저 (샤드 DB에서 실행)
CREATE PROCEDURE GetChatRoomsByUser(
    IN p_user_id INT
)
BEGIN
    SELECT 
        chat_id,
        title,
        domain,
        created_at,
        updated_at
    FROM chat_room 
    WHERE user_id = p_user_id AND is_active = TRUE
    ORDER BY updated_at DESC;
END //

-- 새 채팅방 생성 프로시저 (샤드 DB에서 실행)
CREATE PROCEDURE CreateChatRoom(
    IN p_user_id INT,
    IN p_title VARCHAR(200),
    OUT p_chat_id INT
)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        RESIGNAL;
    END;
    
    START TRANSACTION;
    
    INSERT INTO chat_room (user_id, title) 
    VALUES (p_user_id, p_title);
    
    SET p_chat_id = LAST_INSERT_ID();
    
    -- 사용자 통계 업데이트 (있다면)
    INSERT INTO user_chat_stats (user_id, total_rooms, last_activity) 
    VALUES (p_user_id, 1, NOW())
    ON DUPLICATE KEY UPDATE 
        total_rooms = total_rooms + 1,
        last_activity = NOW();
    
    -- 결과 반환 (chatbot_template_impl.py에서 사용)
    SELECT p_chat_id;
    
    COMMIT;
END //

DELIMITER ;

-- ================================================================
-- 3. SHARD DATABASE SCHEMA (medichain_shard_0, medichain_shard_1, ...)
-- ================================================================

-- 샤드 DB 생성 (예시: 2개 샤드)
CREATE DATABASE IF NOT EXISTS medichain_shard_0;
CREATE DATABASE IF NOT EXISTS medichain_shard_1;

-- 각 샤드에 동일한 스키마 적용
USE medichain_shard_0;

-- 채팅방 테이블 (실제 코드에서 chat_room 사용)
CREATE TABLE chat_room (
    chat_id INT PRIMARY KEY AUTO_INCREMENT,  -- 코드에서 chat_id 컬럼명 사용
    user_id INT NOT NULL COMMENT '글로벌 DB의 user_id',
    title VARCHAR(200) NOT NULL COMMENT '채팅방 제목',
    domain VARCHAR(50) DEFAULT 'general' COMMENT '의료 도메인 (clinic, drug, emergency, etc.)',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    
    INDEX idx_user_id (user_id),
    INDEX idx_user_created (user_id, created_at),
    INDEX idx_domain (domain)
);

-- 채팅 메시지 테이블
CREATE TABLE chat_messages (
    message_id INT PRIMARY KEY AUTO_INCREMENT,
    chat_id INT NOT NULL,  -- room_id 대신 chat_id 사용
    user_id INT NOT NULL COMMENT '글로벌 DB의 user_id',
    role ENUM('user', 'bot') NOT NULL COMMENT '메시지 발신자',
    content TEXT NOT NULL COMMENT '메시지 내용',
    message_type VARCHAR(50) DEFAULT 'text' COMMENT '메시지 타입',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (chat_id) REFERENCES chat_room(chat_id) ON DELETE CASCADE,
    INDEX idx_chat_created (chat_id, created_at),
    INDEX idx_user_time (user_id, created_at),
    INDEX idx_role (role)
);

-- 사용자 대화 통계 테이블 (선택사항)
CREATE TABLE user_chat_stats (
    user_id INT PRIMARY KEY,
    total_rooms INT DEFAULT 0,
    total_messages INT DEFAULT 0,
    last_activity TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- shard_1에도 동일한 테이블 생성
USE medichain_shard_1;

CREATE TABLE chat_room (
    chat_id INT PRIMARY KEY AUTO_INCREMENT,  -- 코드에서 chat_id 컬럼명 사용
    user_id INT NOT NULL COMMENT '글로벌 DB의 user_id',
    title VARCHAR(200) NOT NULL COMMENT '채팅방 제목',
    domain VARCHAR(50) DEFAULT 'general' COMMENT '의료 도메인 (clinic, drug, emergency, etc.)',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    
    INDEX idx_user_id (user_id),
    INDEX idx_user_created (user_id, created_at),
    INDEX idx_domain (domain)
);

CREATE TABLE chat_messages (
    message_id INT PRIMARY KEY AUTO_INCREMENT,
    chat_id INT NOT NULL,  -- room_id 대신 chat_id 사용
    user_id INT NOT NULL COMMENT '글로벌 DB의 user_id',
    role ENUM('user', 'bot') NOT NULL COMMENT '메시지 발신자',
    content TEXT NOT NULL COMMENT '메시지 내용',
    message_type VARCHAR(50) DEFAULT 'text' COMMENT '메시지 타입',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (chat_id) REFERENCES chat_room(chat_id) ON DELETE CASCADE,
    INDEX idx_chat_created (chat_id, created_at),
    INDEX idx_user_time (user_id, created_at),
    INDEX idx_role (role)
);

CREATE TABLE user_chat_stats (
    user_id INT PRIMARY KEY,
    total_rooms INT DEFAULT 0,
    total_messages INT DEFAULT 0,
    last_activity TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- ================================================================
-- 4. SAMPLE DATA (테스트용 데이터)
-- ================================================================

USE medichain_global;

-- 샤드 정보 등록
INSERT INTO shard_info (shard_id, host, port, database_name, username, password, is_active) VALUES
(0, 'localhost', 3306, 'medichain_shard_0', 'root', 'password', 1),
(1, 'localhost', 3306, 'medichain_shard_1', 'root', 'password', 1);

-- 테스트 사용자 생성 예시
-- CALL RegisterUser('test_user', '', SHA2('password123salt_hex', 256), 'salt_hex', 2);
-- CALL RegisterUser('admin', '', SHA2('admin123salt_hex2', 256), 'salt_hex2', 2);

-- ================================================================
-- 5. USEFUL QUERIES (개발/디버깅용)
-- ================================================================

-- 사용자 정보 조회
-- SELECT u.user_id, u.username, u.created_at, usm.shard_id 
-- FROM users u 
-- JOIN user_shard_mapping usm ON u.user_id = usm.user_id 
-- WHERE u.username = 'test_user';

-- 샤드별 사용자 분포 확인
-- SELECT shard_id, COUNT(*) as user_count 
-- FROM user_shard_mapping 
-- GROUP BY shard_id;

-- 특정 사용자의 채팅방 목록 (샤드 DB에서)
-- SELECT room_id, title, domain, created_at 
-- FROM chat_rooms 
-- WHERE user_id = ? AND is_active = 1 
-- ORDER BY updated_at DESC;

-- 특정 채팅방의 메시지 히스토리 (샤드 DB에서)
-- SELECT role, content, created_at 
-- FROM chat_messages 
-- WHERE room_id = ? 
-- ORDER BY created_at ASC 
-- LIMIT 50;

-- ================================================================
-- Redis Key Patterns (참고용)
-- ================================================================
-- accessToken:{uuid} -> platform_id (TTL: 3600초)
-- sessionInfo:{uuid} -> JSON(SessionInfo) (TTL: 3600초)  
-- chat_history:{user_id}:{room_id} -> LIST of JSON messages (최근 50개)
-- conversation:{user_id} -> JSON context (TTL: 3600초)
/*
 Navicat Premium Data Transfer

 Source Server         : Base de Datos 2
 Source Server Type    : MySQL
 Source Server Version : 80042 (8.0.42)
 Source Host           : localhost:3306
 Source Schema         : sistema_cursos

 Target Server Type    : MySQL
 Target Server Version : 80042 (8.0.42)
 File Encoding         : 65001

 Date: 25/05/2025 18:16:39
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for curso
-- ----------------------------
DROP TABLE IF EXISTS `curso`;
CREATE TABLE `curso`  (
  `id_curso` int NOT NULL AUTO_INCREMENT,
  `titulo` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `descripcion` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `fecha_inicio` date NOT NULL,
  `fecha_fin` date NOT NULL,
  `id_usuario` int NOT NULL,
  PRIMARY KEY (`id_curso`) USING BTREE,
  INDEX `id_usuario`(`id_usuario` ASC) USING BTREE,
  CONSTRAINT `curso_ibfk_1` FOREIGN KEY (`id_usuario`) REFERENCES `usuario` (`id_usuario`) ON DELETE CASCADE ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 5 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of curso
-- ----------------------------
INSERT INTO `curso` VALUES (1, 'Curso de SQL Básico', 'Aprende SQL desde cero', '2025-06-01', '2025-07-31', 4);
INSERT INTO `curso` VALUES (2, 'Curso de HTML y CSS', 'Diseño web básico', '2025-06-15', '2025-08-01', 5);
INSERT INTO `curso` VALUES (3, 'Curso de Python', 'Aprende python desde 0', '2025-06-02', '2025-08-01', 6);
INSERT INTO `curso` VALUES (4, 'Curso de TypeScript', 'Aprende desde 0 TypeScript', '2025-06-02', '2025-08-01', 5);

-- ----------------------------
-- Table structure for evaluacion
-- ----------------------------
DROP TABLE IF EXISTS `evaluacion`;
CREATE TABLE `evaluacion`  (
  `id_evaluacion` int NOT NULL AUTO_INCREMENT,
  `tipo` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `nota` int NOT NULL,
  `id_leccion` int NOT NULL,
  `id_usuario` int NOT NULL,
  PRIMARY KEY (`id_evaluacion`) USING BTREE,
  INDEX `id_leccion`(`id_leccion` ASC) USING BTREE,
  INDEX `id_usuario`(`id_usuario` ASC) USING BTREE,
  CONSTRAINT `evaluacion_ibfk_1` FOREIGN KEY (`id_leccion`) REFERENCES `leccion` (`id_leccion`) ON DELETE CASCADE ON UPDATE RESTRICT,
  CONSTRAINT `evaluacion_ibfk_2` FOREIGN KEY (`id_usuario`) REFERENCES `usuario` (`id_usuario`) ON DELETE CASCADE ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 25 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of evaluacion
-- ----------------------------
INSERT INTO `evaluacion` VALUES (1, 'examen', 80, 1, 1);
INSERT INTO `evaluacion` VALUES (2, 'tarea', 90, 1, 1);
INSERT INTO `evaluacion` VALUES (3, 'proyecto', 85, 2, 1);
INSERT INTO `evaluacion` VALUES (4, 'examen', 75, 1, 2);
INSERT INTO `evaluacion` VALUES (5, 'tarea', 80, 1, 2);
INSERT INTO `evaluacion` VALUES (6, 'proyecto', 70, 2, 2);
INSERT INTO `evaluacion` VALUES (7, 'examen', 90, 1, 3);
INSERT INTO `evaluacion` VALUES (8, 'tarea', 95, 1, 3);
INSERT INTO `evaluacion` VALUES (9, 'proyecto', 92, 2, 3);
INSERT INTO `evaluacion` VALUES (10, 'examen', 78, 3, 1);
INSERT INTO `evaluacion` VALUES (11, 'tarea', 88, 3, 1);
INSERT INTO `evaluacion` VALUES (12, 'proyecto', 82, 4, 1);
INSERT INTO `evaluacion` VALUES (13, 'examen', 68, 3, 2);
INSERT INTO `evaluacion` VALUES (14, 'tarea', 70, 3, 2);
INSERT INTO `evaluacion` VALUES (15, 'proyecto', 72, 4, 2);
INSERT INTO `evaluacion` VALUES (16, 'examen', 88, 3, 3);
INSERT INTO `evaluacion` VALUES (17, 'tarea', 84, 3, 3);
INSERT INTO `evaluacion` VALUES (18, 'proyecto', 90, 4, 3);
INSERT INTO `evaluacion` VALUES (19, 'examen', 85, 5, 1);
INSERT INTO `evaluacion` VALUES (20, 'quiz', 60, 5, 1);
INSERT INTO `evaluacion` VALUES (21, 'tarea', 50, 5, 1);
INSERT INTO `evaluacion` VALUES (22, 'examen', 100, 6, 1);
INSERT INTO `evaluacion` VALUES (23, 'examen', 96, 7, 10);
INSERT INTO `evaluacion` VALUES (24, 'examen', 96, 7, 10);

-- ----------------------------
-- Table structure for inscripcion
-- ----------------------------
DROP TABLE IF EXISTS `inscripcion`;
CREATE TABLE `inscripcion`  (
  `id_inscripcion` int NOT NULL AUTO_INCREMENT,
  `id_usuario` int NOT NULL,
  `id_curso` int NOT NULL,
  `fecha_inscripcion` date NOT NULL,
  `estado` enum('activa','inactiva') CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  PRIMARY KEY (`id_inscripcion`) USING BTREE,
  INDEX `id_usuario`(`id_usuario` ASC) USING BTREE,
  INDEX `id_curso`(`id_curso` ASC) USING BTREE,
  CONSTRAINT `inscripcion_ibfk_1` FOREIGN KEY (`id_usuario`) REFERENCES `usuario` (`id_usuario`) ON DELETE CASCADE ON UPDATE RESTRICT,
  CONSTRAINT `inscripcion_ibfk_2` FOREIGN KEY (`id_curso`) REFERENCES `curso` (`id_curso`) ON DELETE CASCADE ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 10 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of inscripcion
-- ----------------------------
INSERT INTO `inscripcion` VALUES (1, 1, 1, '2025-06-02', 'activa');
INSERT INTO `inscripcion` VALUES (2, 1, 2, '2025-06-20', 'activa');
INSERT INTO `inscripcion` VALUES (3, 2, 1, '2025-06-03', 'activa');
INSERT INTO `inscripcion` VALUES (4, 2, 2, '2025-06-21', 'activa');
INSERT INTO `inscripcion` VALUES (5, 3, 1, '2025-06-04', 'activa');
INSERT INTO `inscripcion` VALUES (6, 3, 2, '2025-06-22', 'activa');
INSERT INTO `inscripcion` VALUES (7, 4, 4, '2025-05-25', 'activa');
INSERT INTO `inscripcion` VALUES (8, 1, 3, '2025-05-25', 'activa');
INSERT INTO `inscripcion` VALUES (9, 10, 4, '2025-05-25', 'activa');

-- ----------------------------
-- Table structure for leccion
-- ----------------------------
DROP TABLE IF EXISTS `leccion`;
CREATE TABLE `leccion`  (
  `id_leccion` int NOT NULL AUTO_INCREMENT,
  `titulo` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `contenido` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `id_curso` int NOT NULL,
  PRIMARY KEY (`id_leccion`) USING BTREE,
  INDEX `id_curso`(`id_curso` ASC) USING BTREE,
  CONSTRAINT `leccion_ibfk_1` FOREIGN KEY (`id_curso`) REFERENCES `curso` (`id_curso`) ON DELETE CASCADE ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 8 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of leccion
-- ----------------------------
INSERT INTO `leccion` VALUES (1, 'Introducción SQL', 'Contenido lección 1', 1);
INSERT INTO `leccion` VALUES (2, 'SELECT y WHERE', 'Contenido lección 2', 1);
INSERT INTO `leccion` VALUES (3, 'Estructura HTML', 'Contenido lección 1', 2);
INSERT INTO `leccion` VALUES (4, 'Estilos con CSS', 'Contenido lección 2', 2);
INSERT INTO `leccion` VALUES (5, 'Declarar Variables', '', 3);
INSERT INTO `leccion` VALUES (6, 'Ciclos', 'Explicación del ciclo while y for.', 3);
INSERT INTO `leccion` VALUES (7, 'Conexion con HTML', 'Conexión entre HTML y CSS, para desarrollo web', 4);

-- ----------------------------
-- Table structure for nota
-- ----------------------------
DROP TABLE IF EXISTS `nota`;
CREATE TABLE `nota`  (
  `id_nota` int NOT NULL AUTO_INCREMENT,
  `id_usuario` int NOT NULL,
  `id_curso` int NOT NULL,
  `nota_final` decimal(5, 2) NOT NULL,
  PRIMARY KEY (`id_nota`) USING BTREE,
  INDEX `id_usuario`(`id_usuario` ASC) USING BTREE,
  INDEX `id_curso`(`id_curso` ASC) USING BTREE,
  CONSTRAINT `nota_ibfk_1` FOREIGN KEY (`id_usuario`) REFERENCES `usuario` (`id_usuario`) ON DELETE CASCADE ON UPDATE RESTRICT,
  CONSTRAINT `nota_ibfk_2` FOREIGN KEY (`id_curso`) REFERENCES `curso` (`id_curso`) ON DELETE CASCADE ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 9 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of nota
-- ----------------------------
INSERT INTO `nota` VALUES (1, 1, 1, 85.00);
INSERT INTO `nota` VALUES (2, 2, 1, 75.00);
INSERT INTO `nota` VALUES (3, 3, 1, 92.33);
INSERT INTO `nota` VALUES (4, 1, 2, 82.67);
INSERT INTO `nota` VALUES (5, 2, 2, 70.00);
INSERT INTO `nota` VALUES (6, 3, 2, 87.33);
INSERT INTO `nota` VALUES (7, 1, 3, 73.75);
INSERT INTO `nota` VALUES (8, 10, 4, 96.00);

-- ----------------------------
-- Table structure for usuario
-- ----------------------------
DROP TABLE IF EXISTS `usuario`;
CREATE TABLE `usuario`  (
  `id_usuario` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `apellido` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `email` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `tipo_usuario` enum('estudiante','docente') CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `contraseña` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  PRIMARY KEY (`id_usuario`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 13 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of usuario
-- ----------------------------
INSERT INTO `usuario` VALUES (1, 'Ana', 'Gómez', 'ana@gmail.com', 'estudiante', 'ana123');
INSERT INTO `usuario` VALUES (2, 'Luis', 'Pérez', 'luis@gmail.com', 'estudiante', 'luis123');
INSERT INTO `usuario` VALUES (3, 'Marta', 'Suárez', 'marta@gmail.com', 'estudiante', 'marta123');
INSERT INTO `usuario` VALUES (4, 'Carlos', 'Ramírez', 'carlos@gmail.com', 'docente', 'carlos123');
INSERT INTO `usuario` VALUES (5, 'Julia', 'Martínez', 'julia@gmail.com', 'docente', 'julia123');
INSERT INTO `usuario` VALUES (6, 'Juan', 'Perez', 'juan@gmail.com', 'estudiante', 'juan123');
INSERT INTO `usuario` VALUES (7, 'Andres', 'Sanchez', 'andres@gmail.com', 'estudiante', 'andres123');
INSERT INTO `usuario` VALUES (8, 'Andres', 'Sanchez', 'andres@gmail.com', 'estudiante', 'andres123');
INSERT INTO `usuario` VALUES (9, 'Andres', 'Sanchez', 'andres@gmail.com', 'estudiante', 'andres123');
INSERT INTO `usuario` VALUES (10, 'Pablo', 'Fernandez', 'pablo@gmail.com', 'estudiante', 'pablo123');
INSERT INTO `usuario` VALUES (11, 'Lucas', 'Chavez', 'lucas@gmail.com', 'docente', 'lucas123');
INSERT INTO `usuario` VALUES (12, 'Reynaldo', 'Arteaga', 'reynaldo@gmail.com', 'estudiante', 'reynaldo123');

-- ----------------------------
-- View structure for vista_alumnos_por_curso
-- ----------------------------
DROP VIEW IF EXISTS `vista_alumnos_por_curso`;
CREATE ALGORITHM = UNDEFINED SQL SECURITY DEFINER VIEW `vista_alumnos_por_curso` AS select `c`.`id_curso` AS `id_curso`,`c`.`titulo` AS `curso`,`c`.`fecha_inicio` AS `fecha_inicio`,`c`.`fecha_fin` AS `fecha_fin`,concat(`docente`.`nombre`,' ',`docente`.`apellido`) AS `docente`,`u`.`id_usuario` AS `id_alumno`,`u`.`nombre` AS `nombre_alumno`,`u`.`apellido` AS `apellido_alumno`,`u`.`email` AS `email_alumno`,`i`.`fecha_inscripcion` AS `fecha_inscripcion`,`i`.`estado` AS `estado`,`n`.`nota_final` AS `nota_final` from ((((`curso` `c` join `usuario` `docente` on((`c`.`id_usuario` = `docente`.`id_usuario`))) join `inscripcion` `i` on((`c`.`id_curso` = `i`.`id_curso`))) join `usuario` `u` on((`i`.`id_usuario` = `u`.`id_usuario`))) left join `nota` `n` on(((`u`.`id_usuario` = `n`.`id_usuario`) and (`c`.`id_curso` = `n`.`id_curso`)))) where (`u`.`tipo_usuario` = 'estudiante');

-- ----------------------------
-- Procedure structure for GuardarCurso
-- ----------------------------
DROP PROCEDURE IF EXISTS `GuardarCurso`;
delimiter ;;
CREATE PROCEDURE `GuardarCurso`(IN p_titulo VARCHAR(50),
    IN p_descripcion TEXT,
    IN p_fecha_inicio DATE,
    IN p_fecha_fin DATE,
    IN p_id_usuario INT)
BEGIN
    INSERT INTO Curso (titulo, descripcion, fecha_inicio, fecha_fin, id_usuario)
    VALUES (p_titulo, p_descripcion, p_fecha_inicio, p_fecha_fin, p_id_usuario);
END
;;
delimiter ;

-- ----------------------------
-- Procedure structure for GuardarEvaluacion
-- ----------------------------
DROP PROCEDURE IF EXISTS `GuardarEvaluacion`;
delimiter ;;
CREATE PROCEDURE `GuardarEvaluacion`(IN p_tipo VARCHAR(20),
    IN p_nota INT,
    IN p_id_leccion INT,
    IN p_id_usuario INT)
BEGIN
    INSERT INTO Evaluacion (tipo, nota, id_leccion, id_usuario)
    VALUES (p_tipo, p_nota, p_id_leccion, p_id_usuario);
END
;;
delimiter ;

-- ----------------------------
-- Procedure structure for GuardarInscripcion
-- ----------------------------
DROP PROCEDURE IF EXISTS `GuardarInscripcion`;
delimiter ;;
CREATE PROCEDURE `GuardarInscripcion`(IN p_id_usuario INT,
    IN p_id_curso INT,
    IN p_fecha_inscripcion DATE,
    IN p_estado ENUM('activa', 'inactiva'))
BEGIN
    INSERT INTO Inscripcion (id_usuario, id_curso, fecha_inscripcion, estado)
    VALUES (p_id_usuario, p_id_curso, p_fecha_inscripcion, p_estado);
END
;;
delimiter ;

-- ----------------------------
-- Procedure structure for GuardarLeccion
-- ----------------------------
DROP PROCEDURE IF EXISTS `GuardarLeccion`;
delimiter ;;
CREATE PROCEDURE `GuardarLeccion`(IN p_titulo VARCHAR(20),
    IN p_contenido TEXT,
    IN p_id_curso INT)
BEGIN
    INSERT INTO Leccion (titulo, contenido, id_curso)
    VALUES (p_titulo, p_contenido, p_id_curso);
END
;;
delimiter ;

-- ----------------------------
-- Procedure structure for GuardarUsuario
-- ----------------------------
DROP PROCEDURE IF EXISTS `GuardarUsuario`;
delimiter ;;
CREATE PROCEDURE `GuardarUsuario`(IN p_nombre VARCHAR(50),
    IN p_apellido VARCHAR(50),
    IN p_email VARCHAR(50),
    IN p_tipo_usuario ENUM('estudiante', 'docente'),
    IN p_contraseña VARCHAR(30))
BEGIN
    INSERT INTO Usuario (nombre, apellido, email, tipo_usuario, contraseña)
    VALUES (p_nombre, p_apellido, p_email, p_tipo_usuario, p_contraseña);
END
;;
delimiter ;

-- ----------------------------
-- Procedure structure for NotaPorAlumno
-- ----------------------------
DROP PROCEDURE IF EXISTS `NotaPorAlumno`;
delimiter ;;
CREATE PROCEDURE `NotaPorAlumno`(IN p_id_usuario INT)
BEGIN
    SELECT 
        u.id_usuario,
        CONCAT(u.nombre, ' ', u.apellido) AS nombre_completo,
        c.id_curso,
        c.titulo AS curso,
        ROUND(AVG(e.nota), 2) AS promedio_notas
    FROM Evaluacion e
    INNER JOIN Usuario u ON e.id_usuario = u.id_usuario
    INNER JOIN Leccion l ON e.id_leccion = l.id_leccion
    INNER JOIN Curso c ON l.id_curso = c.id_curso
    WHERE u.id_usuario = p_id_usuario
    GROUP BY u.id_usuario, u.nombre, u.apellido, c.id_curso, c.titulo;
END
;;
delimiter ;

-- ----------------------------
-- Procedure structure for NotasPorCurso
-- ----------------------------
DROP PROCEDURE IF EXISTS `NotasPorCurso`;
delimiter ;;
CREATE PROCEDURE `NotasPorCurso`(IN p_id_curso INT)
BEGIN
    SELECT 
        c.id_curso,
        c.titulo AS curso,
        u.id_usuario,
        CONCAT(u.nombre, ' ', u.apellido) AS nombre_completo,
        ROUND(AVG(e.nota), 2) AS promedio_alumno
    FROM Evaluacion e
    INNER JOIN Usuario u ON e.id_usuario = u.id_usuario
    INNER JOIN Leccion l ON e.id_leccion = l.id_leccion
    INNER JOIN Curso c ON l.id_curso = c.id_curso
    WHERE c.id_curso = p_id_curso
    GROUP BY 
        c.id_curso, c.titulo,
        u.id_usuario, u.nombre, u.apellido;
END
;;
delimiter ;

-- ----------------------------
-- Triggers structure for table evaluacion
-- ----------------------------
DROP TRIGGER IF EXISTS `actualizar_nota_final`;
delimiter ;;
CREATE TRIGGER `actualizar_nota_final` AFTER INSERT ON `evaluacion` FOR EACH ROW BEGIN
    DECLARE promedio DECIMAL(5,2);

    SELECT AVG(nota)
    INTO promedio
    FROM Evaluacion
    WHERE id_usuario = NEW.id_usuario
      AND id_leccion IN (
          SELECT id_leccion FROM Leccion
          WHERE id_curso = (
              SELECT id_curso FROM Leccion WHERE id_leccion = NEW.id_leccion
          )
      );

    IF EXISTS (
        SELECT 1 FROM Nota
        WHERE id_usuario = NEW.id_usuario
          AND id_curso = (
              SELECT id_curso FROM Leccion WHERE id_leccion = NEW.id_leccion
          )
    ) THEN
        UPDATE Nota
        SET nota_final = promedio
        WHERE id_usuario = NEW.id_usuario
          AND id_curso = (
              SELECT id_curso FROM Leccion WHERE id_leccion = NEW.id_leccion
          );
    ELSE
        INSERT INTO Nota(id_usuario, id_curso, nota_final)
        VALUES (
            NEW.id_usuario,
            (SELECT id_curso FROM Leccion WHERE id_leccion = NEW.id_leccion),
            promedio
        );
    END IF;
END
;;
delimiter ;

-- ----------------------------
-- Triggers structure for table evaluacion
-- ----------------------------
DROP TRIGGER IF EXISTS `recalcular_nota_final_borrado`;
delimiter ;;
CREATE TRIGGER `recalcular_nota_final_borrado` AFTER DELETE ON `evaluacion` FOR EACH ROW BEGIN
    DECLARE promedio DECIMAL(5,2);

    SELECT AVG(nota)
    INTO promedio
    FROM Evaluacion
    WHERE id_usuario = OLD.id_usuario
      AND id_leccion IN (
          SELECT id_leccion FROM Leccion
          WHERE id_curso = (
              SELECT id_curso FROM Leccion WHERE id_leccion = OLD.id_leccion
          )
      );

    UPDATE Nota
    SET nota_final = IFNULL(promedio, 0)
    WHERE id_usuario = OLD.id_usuario
      AND id_curso = (
          SELECT id_curso FROM Leccion WHERE id_leccion = OLD.id_leccion
      );
END
;;
delimiter ;

-- ----------------------------
-- Triggers structure for table inscripcion
-- ----------------------------
DROP TRIGGER IF EXISTS `evitar_inscripcion_duplicada`;
delimiter ;;
CREATE TRIGGER `evitar_inscripcion_duplicada` BEFORE INSERT ON `inscripcion` FOR EACH ROW BEGIN
    IF EXISTS (
        SELECT 1 FROM Inscripcion
        WHERE id_usuario = NEW.id_usuario
          AND id_curso = NEW.id_curso
    ) THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'El usuario ya está inscrito en este curso';
    END IF;
END
;;
delimiter ;

SET FOREIGN_KEY_CHECKS = 1;

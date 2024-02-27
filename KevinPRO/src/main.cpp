#include "main.h"
#include "lemlib/api.hpp"

////////////////////////////////////////////////////////////
//Constructors//////////////////////////////////////////////
////////////////////////////////////////////////////////////

pros::Controller master (E_CONTROLLER_MASTER);//controller

pros::Motor spinner(12, pros::E_MOTOR_GEARSET_06, false);//spinner

pros::Motor RLifter(3, pros::E_MOTOR_GEARSET_36, false, E_MOTOR_ENCODER_DEGREES);//Right Lifter Motor
pros::Motor LLifter(13, pros::E_MOTOR_GEARSET_36, true, E_MOTOR_ENCODER_DEGREES);//Left Lifter Motor
	pros::Motor_Group lifter({RLifter, LLifter});

#define  RIGHT_WING 'D'//RightWing port
pros::ADIDigitalOut rightWing(RIGHT_WING); //rightwing

#define  LEFT_WING 'H'//leftwing port
pros::ADIDigitalOut leftWing(LEFT_WING);//lefting

#define  BUMPER_SWITCH_1 'B'//bumper1 port
pros::ADIDigitalIn bumperSwitch1(BUMPER_SWITCH_1);//bumper 1

#define  BUMPER_SWITCH_2 'G'//bumper2 port
pros::ADIDigitalIn bumperSwitch2(BUMPER_SWITCH_2); //bumper 2

#define  BLOCKER 'C'//blocker port
pros::ADIDigitalOut blocker(BLOCKER); //blocker

#define  RATCHEt 'A'//rachet port
pros::ADIDigitalOut ratchet(RATCHEt);//rachet


//LEFT MOTORS
pros::Motor LeftFront(17, pros::E_MOTOR_GEARSET_18, true, E_MOTOR_ENCODER_DEGREES);//Front left
pros::Motor LeftMiddle(18, pros::E_MOTOR_GEARSET_18, true, E_MOTOR_ENCODER_DEGREES);//Middle Left
pros::Motor LeftBack(19, pros::E_MOTOR_GEARSET_18, true, E_MOTOR_ENCODER_DEGREES);//Back Left
	pros::Motor_Group left_side({LeftFront, LeftMiddle, LeftBack});// left Motor Group

//RIGHT MOTORE
pros::Motor RightFront(7, pros::E_MOTOR_GEARSET_18, false, E_MOTOR_ENCODER_DEGREES);// Front Right
pros::Motor RightMiddle(8, pros::E_MOTOR_GEARSET_18, false, E_MOTOR_ENCODER_DEGREES);// Middle Right
pros::Motor RightBack(9, pros::E_MOTOR_GEARSET_18, false, E_MOTOR_ENCODER_DEGREES);//Back Right
	pros::Motor_Group right_side({RightFront, RightMiddle, RightBack});//right motor group


////////////////////////////////////////////////////////////
//PID LEMLIB////////////////////////////////////////////////
////////////////////////////////////////////////////////////



//driveTrain_t
lemlib::Drivetrain_t drivetrain {
	&left_side, // left side
	&right_side, // right side
	12.962, // trake width
	3.25,// wheel diameter
	333// wheel rpm
};

//left Side
lemlib::TrackingWheel left_tracking(
	&left_side,//Look at left side of ther robots rotation 
	3.25, // wheel diamter
	-6.5, //center ofset
	334 //v max rpms
);

//right Side
lemlib::TrackingWheel right_tracking(
	&right_side,//Look at left side of ther robots rotation 
	3.25, // wheel diamter
	6.5, //center ofset
	334 //max rpms
);

//inirttal activate
pros::Imu inertial(6);

//Odemetry
lemlib::OdomSensors_t sensors {
	&left_tracking, //left side tracking
	&right_tracking, //right side tracking
	nullptr, //no horizontal tracking
	nullptr, //no horizontal trackinhg
	&inertial // inirtial sensor
};

// forward/backward PID
lemlib::ChassisController_t lateralController {
    8, // kP
    30, // kD
    1, // smallErrorRange
    100, // smallErrorTimeout
    3, // largeErrorRange
    500, // largeErrorTimeout
    5 // slew rate
};
 
// turning PID
lemlib::ChassisController_t angularController {
    4, // kP
    40, // kD
    1, // smallErrorRange
    100, // smallErrorTimeout
    3, // largeErrorRange
    500, // largeErrorTimeout
    40 // slew rate
};

//identify chassis
lemlib::Chassis chassis(drivetrain, lateralController, angularController, sensors);

////////////////////////////////////////////////////////////
//Variables/////////////////////////////////////////////////
////////////////////////////////////////////////////////////

//the number of autons we have
const int auton_nums = 2;

//the current auton selected
int auton = 2;

//tells if its blockinh
bool blocking = false;

//what is the spin mode
std::string spin_mode = "OFF";
//the height level of th robot
int height = 0;
int spin_direction = 1;
std::string spin_simb = "";


void display() {
	//loop forever
	while (true) {
        lemlib::Pose pose = chassis.getPose(); // get the current position of the robot
        pros::lcd::print(0, "x: %f", pose.x); // print the x position
        pros::lcd::print(1, "y: %f", pose.y); // print the y position
        pros::lcd::print(2, "heading: %f", pose.theta); // print the heading
        
		if (auton == 1) {
			pros::lcd::print(6, "Jenga"); // print the heading
			master.set_text(1, 0, std::string("Jenga  " + spin_mode));

		}
		if (auton == 2) {
			pros::lcd::print(6, "DEFFENCE "); // print the heading
			master.set_text(1, 0, "DEFFENCE  %c" + spin_mode);
		}

		pros::delay(50);
    }
}

void on_left_button() {
	auton--;
	if (auton <= 0){
		auton = auton_nums;
	}
}

void on_center_button() {
	auton++;
	if (auton > auton_nums){
		auton = 1;
	}
}

void on_right_button() {
	
}


void direction() {
	if (height == 0 or height == 1) {
		spin_direction = -1;
	}
    if (height == 2 or height == 3) {
        spin_direction = 1;
	}
}

void reverseSpin() {


	spin_direction = spin_direction * -1;
	if (spin_simb == "") {
		spin_simb = "-";left_side.set_brake_modes(pros::E_MOTOR_BRAKE_HOLD);
	}
	else {
		spin_simb = "";
	}	
	spinner.brake();
}


void hightenator() {
	while (true) {

		if (master.get_digital_new_press(pros::E_CONTROLLER_DIGITAL_R2)){
			if (height < 3){
				height++;
				spin_simb = "";
				direction();
			}
        }

		if (master.get_digital_new_press(pros::E_CONTROLLER_DIGITAL_L2)){
			if (height > 0){
				height--;
				spin_simb = "";
				direction();
			}
        }

		if (master.get_digital_new_press(pros::E_CONTROLLER_DIGITAL_LEFT)){
			height = 0;
			ratchet.set_value(false);
			
        }
		
		if (master.get_digital_new_press(pros::E_CONTROLLER_DIGITAL_RIGHT)){
			height = 420;
		}

		if (height == 0) {
			spinner.move(spin_direction * 50);

			spin_mode = spin_simb + "Push Over";

			while (bumperSwitch1.get_value() == LOW && bumperSwitch2.get_value() == LOW) {
				lifter.move(-100);
			}

			lifter.tare_position();
			lifter.set_brake_modes(pros::E_MOTOR_BRAKE_COAST);
			lifter.brake();
		}

		else if (height == 1) {
			spinner.move(spin_direction * 80);
			lifter.set_brake_modes(pros::E_MOTOR_BRAKE_HOLD);
			spin_mode = spin_simb + "Intake";
			lifter.move_absolute(150,70);
		}

		else if (height == 2) {
			lifter.set_brake_modes(pros::E_MOTOR_BRAKE_HOLD);
			spinner.brake();
			spin_mode = "None";
			lifter.move_absolute(300,70);
		}

		else if (height == 3) {
			lifter.set_brake_modes(pros::E_MOTOR_BRAKE_HOLD);
			spinner.move(spin_direction * 100);
			lifter.move_absolute(590,70);

			spin_mode = spin_simb + "Shooting";

		}
		else if (height == 420){
			spinner.brake();
			lifter.set_brake_modes(pros::E_MOTOR_BRAKE_HOLD);

			if (bumperSwitch1.get_value() == LOW && bumperSwitch2.get_value() == LOW) {
				if (master.get_digital(pros::E_CONTROLLER_DIGITAL_UP)){
					lifter.move(70);
				} else if (master.get_digital(pros::E_CONTROLLER_DIGITAL_DOWN)) {
					lifter.move(-70);
				} else {
					lifter.brake();
				}
			} else {
				ratchet.set_value(true);
			}
        }

		pros::delay(2.5);
	}
}







/**
 * Runs initialization code. This occurs as soon as the program is started.
 *
 * All other competition modes are blocked by initialize; it is recommended
 * to keep execution time for this mode under a few seconds.
 */
void initialize() {
	left_side.set_brake_modes(pros::E_MOTOR_BRAKE_HOLD);
	right_side.set_brake_modes(pros::E_MOTOR_BRAKE_HOLD);
	pros::lcd::initialize(); // initialize brain screen
    chassis.calibrate(); // calibrate the chassis
    pros::Task screenTask(display); // create a task to print the position to the screen
	pros::Task liftCheck(hightenator);
	pros::lcd::register_btn0_cb(on_left_button);
	pros::lcd::register_btn1_cb(on_center_button);
	pros::lcd::register_btn2_cb(on_right_button);
	spinner.set_brake_mode(pros::E_MOTOR_BRAKE_COAST);

	rightWing.set_value(false);
    leftWing.set_value(false);
	blocker.set_value(false);
	ratchet.set_value(false);
}

/**
 * Runs while the robot is in the disabled state of Field Management System or
 * the VEX Competition Switch, following either autonomous or opcontrol. When
 * the robot is enabled, this task will exit.
 */
void disabled() {
//DONT ADD STUFF HERE (UNLESS YOU KNoW WHAT YOUR DOING)
}
/**
 * Runs after initialize(), and before autonomous when connected to the Field
 * Management System or the VEX Competition Switch. This is intended for
 * competition-specific initialization routines, such as an autonomous selector
 * on the LCD.
 *
 * This task will exit when the robot is enabled and autonomous or opcontrol
 * starts.
 */
void competition_initialize() {
	
}

/**
 * Runs the user autonomous code. This function will be started in its own task
 * with the default priority and stack size whenever the robot is enabled via
 * the Field Management System or the VEX Competition Switch in the autonomous
 * mode. Alternatively, this function may be called in initialize or opcontrol
 * for non-competition testing purposes.
 *
 * If the robot is disabled or communications is lost, the autonomous task
 * will be stopped. Re-enabling the robot will restart the task, not re-start it
 * from where it left off.
 */
void autonomous() {
	//SETTING POSITION
	//chassis.setPose(0, 0, 0); // X: 0, Y: 0, Heading: 0

	//TURN TO
	//chassis.turnTo(53, 53, 1000); // turn to the point (53, 53) with a timeout of 1000 ms
    //chassis.turnTo(-20, 32, 1500, true); // turn to the point (-20, 32) with the back of the robot facing the point, and a timeout of 1500 ms
    //chassis.turnTo(10, 0, 1000, false, 50); // turn to the point (10, 0) with a timeout of 1000 ms, and a maximum speed of 50

	//MOVE TO
	//chassis.moveTo(53, 53, 1000); // move to the point (53, 53) with a timeout of 1000 ms
    //chassis.moveTo(10, 0, 1000, 50); // move to the point (10, 0) with a timeout of 1000 ms, and a maximum speed of 50

	if (auton == 1) {
		//start 8.5in
		chassis.setPose(0, 0, 0);
		leftWing.set_value(true);
		chassis.turnTo(-14, -2, 1000, false, 100);
		leftWing.set_value(false);

		chassis.turnTo(15, -6, 500, true);
		chassis.moveTo(15, -6, 500);

		chassis.turnTo(39, -6, 200, true);
		chassis.moveTo(30.5, -6, 1000, 127);

		chassis.turnTo(0, -6, 500, false);
		chassis.moveTo(0, -6, 900);

		chassis.turnTo(-22, 25, 400, false);
		chassis.moveTo(-22, 30, 1100, 127);

		chassis.turnTo(-22, 100, 100, false);
		chassis.moveTo(-22, 100, 100);

		/////////////////////////////////
		chassis.setPose(0, 0, 0);

		chassis.moveTo(0, -8, 500);
		chassis.turnTo(20, -8, 300, true);





		
		

		
	}
	if (auton == 2) {
		//start 8.5in
		
		chassis.setPose(0, 0, 0);
		leftWing.set_value(true);
		chassis.turnTo(-14, -2, 1000, false, 100);
		leftWing.set_value(false);

		chassis.turnTo(15, -6, 500, true);
		chassis.moveTo(15, -6, 500);

		chassis.turnTo(39, -6, 200, true);
		chassis.moveTo(30.5, -6, 1000, 127);

		chassis.turnTo(0, -6, 500, false);
		chassis.moveTo(0, -6, 900);

		chassis.turnTo(-22, 25, 400, false);
		chassis.moveTo(-22, 30, 1100, 127);

		chassis.turnTo(-22, 100, 100, false);
		chassis.moveTo(-22, 100, 100);

		/////////////////////////////////
		chassis.setPose(0, 0, 0);
		
		chassis.moveTo(0, -8, 500);
		
		chassis.turnTo(37, -28, 400,false);
		chassis.moveTo(37, -28, 1000);

		blocker.set_value(true);

		chassis.turnTo(48, -25, 500, false);
		chassis.moveTo(48, -25, 800);
		


	}
	if (auton == 3) {
	}
	if (auton == 4) {
	}
	if (auton == 5) {
	}
	if (auton == 6) {
	}
	if (auton == 7) {
	}
}


/**
 * Runs the operator control code. This function will be started in its own task
 * with the default priority and stack size whenever the robot is enabled via
 * the Field Management System or the VEX Competition Switch in the operator
 * control mode.
 *
 * If no competition control is connected, this function will run immediately
 * following initialize().
 *
 * If the robot is disabled or communications is lost, the
 * operator control task will be stopped. Re-enabling the robot will restart the
 * task, not resume it from where it left off.
 */
void opcontrol() {

	if (auton == 1) {
		height = 3;
	}

	while (true) {
		int move = master.get_analog(pros::E_CONTROLLER_ANALOG_LEFT_Y);

		int turn = master.get_analog(pros::E_CONTROLLER_ANALOG_RIGHT_X);

		if (abs(move) <= 5){move = 0;} 
		if (abs(turn) <= 5){turn = 0;}

		int leftvel = 0;
		int rightvel = 0;

		//left_side.set_voltage_limit(drivelimit);
		//right_side.set_voltage_limit(drivelimit);
		if (abs(move + turn) <= 127) {
			leftvel = move + turn;
		}
		if (abs(move - turn) <= 127) {
			rightvel = move - turn;
		}
		
		left_side.move(leftvel);
		right_side.move(rightvel);

		if (master.get_digital_new_press(pros::E_CONTROLLER_DIGITAL_B)){
			reverseSpin();
        }

		if (master.get_digital(pros::E_CONTROLLER_DIGITAL_R1)){
			rightWing.set_value(true);
        } else {
			rightWing.set_value(false);
		}

		if (master.get_digital(pros::E_CONTROLLER_DIGITAL_L1)){
			leftWing.set_value(true);
        } else {
			leftWing.set_value(false);
		}

		if (master.get_digital_new_press(pros::E_CONTROLLER_DIGITAL_X)){
			if (blocking) {
				blocker.set_value(false);
				blocking = false;
			} else {
				blocker.set_value(true);
				blocking = true;
			}
        }
		// e

		delay(20);




		
	}
}

package Tricycle {

  block Tricycle {
    part Frame;
    part FrontWheel : Wheel;
    part RearWheel_1 : Wheel;
    part RearWheel_2 : Wheel;
    connect FrontWheel.axle to Frame.front_fork;
    connect RearWheel_1.axle to Frame.rear_axle_1;
    connect RearWheel_2.axle to Frame.rear_axle_2;
  }

  block Wheel {
    part Rim;
    part Tire;
    part Axle;
    connect Rim.inner_diameter to Tire.outer_diameter;
    connect Axle.hub to Rim.inner_diameter;
  }

  block Frame {
    part Seat;
    part FrontFork;
    part RearAxle_1;
    part RearAxle_2;
    connect FrontFork.steerer_tube to Seat.seat_post;
    connect RearAxle_1.left_dropout to RearAxle_2.right_dropout;
  }

}
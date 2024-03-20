package 'Rocket Ship' {
    block 'Rocket' {
        value propellantMass :> Mass;
        value thrust :> Force;
        value burnTime :> Time;
        value specificImpulse :> SpecificImpulse;
        value dryMass :> Mass;
        value totalMass :> Mass = dryMass + propellantMass;
        value propellantFlowRate :> MassRate = propellantMass / burnTime;
        value exhaustVelocity :> Velocity = specificImpulse * g0;
        value thrust = propellantFlowRate * exhaustVelocity;
    }
    
    block 'Engine' {
        value thrust :> Force;
        value specificImpulse :> SpecificImpulse;
        value propellantFlowRate :> MassRate;
        value exhaustVelocity :> Velocity = specificImpulse * g0;
        value thrust = propellantFlowRate * exhaustVelocity;
    }
    
    block 'Fuel Tank' {
        value propellantMass :> Mass;
    }
    
    block 'Payload' {
        value payloadMass :> Mass;
    }
    
    block 'Rocket Ship' {
        part engine : Engine;
        part fuelTank : Fuel Tank;
        part payload : Payload;
    }
}

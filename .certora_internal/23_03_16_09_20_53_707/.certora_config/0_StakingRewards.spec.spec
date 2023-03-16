import "./erc20.spec"

using DummyERC20A as stakingToken
using DummyERC20B as rewardsToken
/**************************************************
 *              METHODS DECLARATIONS              *
 **************************************************/
methods{
    stakingToken()                  returns (address)   envfree
    rewardsToken()                  returns (address)   envfree
    owner()                         returns (address)   envfree
    duration()                      returns (uint256)   envfree
    finishAt()                      returns (uint256)   envfree
    updatedAt()                     returns (uint256)   envfree
    rewardRate()                    returns (uint256)   envfree
    rewardPerTokenStored()          returns (uint256)   envfree
    userRewardPerTokenPaid(address) returns (uint256)   envfree
    rewards(address)                returns (uint256)   envfree
    totalSupply()                   returns (uint256)   envfree
    balanceOf(address)              returns (uint256)   envfree
    _min(uint256, uint256)          returns(uint256)    envfree
    rewardsToken.balanceOf(address) returns (uint256)   envfree
    stakingToken.balanceOf(address) returns (uint256)   envfree
    lastTimeRewardApplicable()      returns (uint256)
    rewardPerToken()                returns (uint256)
    earned(address)                 returns uint256
    stake(uint256)
    withdraw(uint256)
    getReward(address)
    setRewardsDuration(uint256)
    notifyRewardAmount(uint256)
}


// rule sanity(env e, method f){
//     calldataarg args;
//     f(e,args);
//     assert false;
// }

// rule whoChangedDuration(method f, env e){
//     uint256 _duration = duration();
//     calldataarg args;
//     f(e, args);
//     uint256 duration_ = duration();
//     assert e.msg.sender!=owner() => _duration == duration_;
// }
// rule integrityOfStake(){
//     env e;uint256 amount;
//     uint256 _balance=balanceOf(e.msg.sender);
//     stake(e,amount);
//     uint256 balance_=balanceOf(e.msg.sender);
//     assert balance_==_balance+amount;
// }
// rule integrityOfWithdraw(){
//     env e;uint256 amount;
//     uint256 _balance=balanceOf(e.msg.sender);
//     withdraw(e,amount);
//     uint256 balance_=balanceOf(e.msg.sender);
//     assert balance_==_balance-amount;
// }


//  ghost mathint totalRewardBalance{
//   init_state axiom totalRewardBalance == 0;
//   }
//  hook Sstore rewards[KEY address addr] uint new_reward (uint256 old_reward) STORAGE {
//     totalRewardBalance = totalRewardBalance + new_reward - old_reward;
//  }

//  //FAILED :- invariant for ensuring the protocol is not insolvent and always has enough reward Token.
// invariant hasEnoughRewardToken()
//     totalRewardBalance<= rewardsToken.balanceOf(currentContract){
//         preserved with (env e){
//             require e.block.timestamp == updatedAt();
//         }
//     }


// finishAt() >= updatedAt() <= block.timestamp
// invariant finishAtAheadOfUpdateAt()
//     finishAt() >=updatedAt()

invariant updateAtLessThanBlockTimestamp(env e)
    updateAt()<=e.block.timestamp


